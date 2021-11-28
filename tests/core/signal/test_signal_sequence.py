import datetime
import unittest
from stock_market.core import add_signal, merge_signals, Signal, SignalSequence, Sentiment

class TestSignalSequence(unittest.TestCase):
						 
	def setUp(self):
		self.name = "TestSignal"
		self.date = datetime.datetime.now().date()
		self.signal = Signal(1, "1", Sentiment.NEUTRAL, self.date)
		self.signal2 = Signal(2, "2", Sentiment.NEUTRAL, self.date)
		self.signal3 = Signal(3, "3", Sentiment.NEUTRAL, self.date + datetime.timedelta(days=1))

	def test_add_signals(self):
		ss = SignalSequence()
		ss = add_signal(ss, self.signal)
		self.assertEqual(ss.signals, [self.signal])
		ss = add_signal(ss, self.signal2)
		self.assertEqual(ss.signals, [self.signal, self.signal2])
		ss = add_signal(ss, self.signal3)
		self.assertEqual(ss.signals, [self.signal, self.signal2, self.signal3])

	def test_merge_signals(self):
		first = SignalSequence()
		first = add_signal(first, self.signal)
		first = add_signal(first, self.signal2)
		first = add_signal(first, self.signal3)

		signal4 = Signal(4, "4", Sentiment.NEUTRAL, self.date - datetime.timedelta(days=1))
		signal5 = Signal(5, "5", Sentiment.NEUTRAL, self.date + datetime.timedelta(days=1))
		signal6 = Signal(6, "6", Sentiment.NEUTRAL, self.date + datetime.timedelta(days=2))
		second = SignalSequence()
		second = add_signal(second, signal4)
		second = add_signal(second, signal5)
		second = add_signal(second, signal6)

		merged = merge_signals(first, second, SignalSequence())
		self.assertEqual(merged.signals, [signal4, self.signal, self.signal2, self.signal3, signal5, signal6])

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