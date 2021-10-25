import datetime
import unittest
from stock_market_engine.core.signal.signal import Signal
from stock_market_engine.core.signal.signal_sequence import SignalSequence

class TestSignalSequence(unittest.TestCase):
						 
	def setUp(self):
		self.name = "TestSignal"
		self.date = datetime.datetime.now().date()
		self.signal = Signal("1", self.date)
		self.signal2 = Signal("2", self.date)
		self.signal3 = Signal("3", self.date + datetime.timedelta(days=1))

	def test_add_and_signals(self):
		ss = SignalSequence()
		ss.add(self.signal)
		self.assertEqual(ss.signals, [self.signal])
		ss.add(self.signal2)
		self.assertEqual(ss.signals, [self.signal, self.signal2])
		ss.add(self.signal3)
		self.assertEqual(ss.signals, [self.signal, self.signal2, self.signal3])

	def test_signals_since(self):
		signals = [self.signal, self.signal2, self.signal3]
		ss = SignalSequence(signals)
		self.assertEqual(ss.signals_since(self.date - datetime.timedelta(days=1)), signals)
		self.assertEqual(ss.signals_since(self.date), [self.signal3])

	def test_eq(self):
		self.assertEqual(SignalSequence(), SignalSequence())
		signals = [self.signal, self.signal2, self.signal3]
		ss = SignalSequence(signals)
		self.assertEqual(ss, ss)
		self.assertNotEqual(ss, SignalSequence())
		self.assertNotEqual(ss, 0)

	def test_json(self):
		signals = [self.signal, self.signal2, self.signal3]
		ss = SignalSequence(signals)
		self.assertEqual(ss, SignalSequence.from_json(ss.to_json()))

if __name__ == '__main__':
    unittest.main()