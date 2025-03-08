import unittest
from analysis.sentiment_analysis import analyze_sentiment

class TestSentimentAnalysis(unittest.TestCase):
    def test_positive_sentiment(self):
        self.assertGreater(analyze_sentiment("I love Python!"), 0)

    def test_negative_sentiment(self):
        self.assertLess(analyze_sentiment("I hate bugs!"), 0)

if __name__ == '__main__':
    unittest.main()