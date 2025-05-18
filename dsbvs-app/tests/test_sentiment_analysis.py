import unittest
from modules.sentiment_analysis import analyze_sentiment

class TestSentimentAnalysis(unittest.TestCase):

    def test_positive_sentiment(self):
        text = "I love this product!"
        polarity, weight = analyze_sentiment(text)
        self.assertGreater(polarity, 0)
        self.assertEqual(weight, 1)

    def test_negative_sentiment(self):
        text = "I hate this product!"
        polarity, weight = analyze_sentiment(text)
        self.assertLess(polarity, 0)
        self.assertEqual(weight, -1)

    def test_neutral_sentiment(self):
        text = "This product is okay."
        polarity, weight = analyze_sentiment(text)
        self.assertEqual(polarity, 0)
        self.assertEqual(weight, 0)

    def test_empty_string(self):
        text = ""
        polarity, weight = analyze_sentiment(text)
        self.assertEqual(polarity, 0)
        self.assertEqual(weight, 0)

if __name__ == '__main__':
    unittest.main()