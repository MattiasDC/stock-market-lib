import copy
import json
from enum import Enum

from transitions import State
from transitions.extensions.markup import MarkupMachine
from utils.functional import Mutable

from stock_market.core import (
    Sentiment,
    Signal,
    SignalDetector,
    SignalSequence,
    Ticker,
    add_signal,
    merge_signals,
)


class EnterOrExit(Enum):

    ENTER = "ENTER"
    EXIT = "EXIT"


class GraphSignalDetectorBuilder:
    def __init__(
        self,
        identifier,
        name=None,
        ticker=None,
        detectors=None,
        state_descriptions=None,
        initial_state=None,
        signal_descriptions=None,
        transitions=None,
    ):
        self.id = identifier
        self.name = name
        self.ticker = ticker
        self.detectors = [] if detectors is None else detectors
        self.state_descriptions = (
            [] if state_descriptions is None else state_descriptions
        )
        self.initial_state = initial_state
        self.signal_descriptions = (
            [] if signal_descriptions is None else signal_descriptions
        )
        self.transitions = [] if transitions is None else transitions

    def set_name(self, name):
        builder = copy.deepcopy(self)
        builder.name = name
        return builder

    def set_ticker(self, ticker):
        builder = copy.deepcopy(self)
        builder.ticker = ticker
        return builder

    def add_detector(self, detector):
        assert detector not in self.detectors
        builder = copy.deepcopy(self)
        builder.detectors.append(detector)
        return builder

    def add_state(self, state_description):
        assert state_description not in self.state_descriptions
        builder = copy.deepcopy(self)
        builder.state_descriptions.append(state_description)
        return builder

    def set_initial_state(self, initial_state):
        assert initial_state in self.state_descriptions
        builder = copy.deepcopy(self)
        builder.initial_state = initial_state
        return builder

    def add_signal_description(self, signal_state, sentiment, enter_or_exit):
        assert signal_state in self.state_descriptions
        signal_description = (signal_state, sentiment, enter_or_exit)
        assert signal_description not in self.signal_states
        builder = copy.deepcopy(self)
        builder.signal_descriptions.append(signal_description)
        return builder

    def add_transition(self, transition):
        assert isinstance(transition, dict)
        assert "source" in transition
        assert "dest" in transition
        assert "trigger" in transition
        assert transition["source"] in self.state_descriptions
        assert transition["dest"] in self.state_descriptions
        assert transition["trigger"] in [d.id for d in self.detectors]

        builder = copy.deepcopy(self)
        builder.transitions.append(transition)
        return builder

    @staticmethod
    def __create_state(state_description, signal_descriptions):
        def __get_signal_factory(sentiment):
            if sentiment == Sentiment.BULLISH:
                return GraphSignalDetector.add_bullish_signal
            elif sentiment == Sentiment.BEARISH:
                return GraphSignalDetector.add_bearish_signal
            assert sentiment == Sentiment.NEUTRAL
            return GraphSignalDetector.add_neutral_signal

        enters = []
        exits = []
        for state, sentiment, enter_or_exit in signal_descriptions:
            if state == state_description:
                if enter_or_exit == EnterOrExit.ENTER:
                    enters.append(__get_signal_factory(sentiment))
                else:
                    assert enter_or_exit == EnterOrExit.EXIT
                    exits.append(__get_signal_factory(sentiment))
        return State(state_description, on_enter=enters, on_exit=exits)

    @staticmethod
    def __create_states(state_descriptions, signal_descriptions):
        return [
            GraphSignalDetectorBuilder.__create_state(s, signal_descriptions)
            for s in state_descriptions
        ]

    @staticmethod
    def __create_machine(
        state_descriptions, initial_state, signal_descriptions, transitions
    ):
        transitions = [t | {"trigger": str(t["trigger"])} for t in transitions]
        return MarkupMachine(
            model=Model(),
            states=GraphSignalDetectorBuilder.__create_states(
                state_descriptions, signal_descriptions
            ),
            initial=initial_state,
            transitions=transitions,
        )

    def build(self):
        return GraphSignalDetector(
            self.id,
            self.name,
            self.ticker,
            self.detectors,
            GraphSignalDetectorBuilder.__create_machine(
                self.state_descriptions,
                self.initial_state,
                self.signal_descriptions,
                self.transitions,
            ),
        )


class Model:
    pass


class GraphSignalDetector(SignalDetector):
    def __init__(
        self,
        identifier,
        name,
        ticker,
        detectors,
        machine,
    ):
        super().__init__(identifier, name)
        self.ticker = ticker
        self.detectors = detectors
        self.machine = machine

    @staticmethod
    def add_state_signal(
        identifier, name, date, ticker, mutable_signal_sequence, sentiment
    ):
        ss = mutable_signal_sequence.get()
        new_ss = add_signal(ss, Signal(identifier, name, sentiment, date, [ticker]))
        mutable_signal_sequence.set(new_ss)

    @staticmethod
    def add_bullish_signal(*args):
        GraphSignalDetector.add_state_signal(*args, Sentiment.BULLISH)

    @staticmethod
    def add_bearish_signal(*args):
        GraphSignalDetector.add_state_signal(*args, Sentiment.BEARISH)

    @staticmethod
    def add_neutral_signal(*args):
        GraphSignalDetector.add_state_signal(*args, Sentiment.NEUTRAL)

    @property
    def __model(self):
        return self.machine.models[0]

    def detect(self, from_date, to_date, stock_market, sequence):
        signals = merge_signals(
            *[
                detector.detect(from_date, to_date, stock_market, SignalSequence())
                for detector in self.detectors
            ]
        )

        mutable_sequence = Mutable(sequence)
        for signal in signals.signals:
            if str(signal.id) not in self.machine.get_triggers(self.__model.state):
                continue
            self.__model.trigger(
                str(signal.id),
                self.id,
                self.name,
                signal.date,
                self.ticker,
                mutable_sequence,
            )

        return mutable_sequence.get()

    def __eq__(self, other):
        if not isinstance(other, GraphSignalDetector):
            return False
        return (self.ticker, sorted(self.detectors), self.machine, self.model,) == (
            other.ticker,
            sorted(other.detectors),
            other.machine,
            other.model,
        )

    @staticmethod
    def NAME():
        return "Graph"

    def to_json(self):
        return json.dumps(
            {
                "id": self.id,
                "name": self.name,
                "ticker": self.ticker.to_json(),
                "signal_detectors": [sd.to_json() for sd in self.detectors],
                "machine": self.machine.markup,
            }
        )

    @staticmethod
    def from_json(json_str, signal_detector_factory):
        json_obj = json.loads(json_str)
        return GraphSignalDetector(
            json_obj["id"],
            json_obj["name"],
            Ticker.from_json(json_obj["ticker"]),
            [
                signal_detector_factory.create(config["name"], config["config"])
                for config in json_obj["signal_detectors"]
            ],
            MarkupMachine(markup=json_obj["machine"]),
        )
