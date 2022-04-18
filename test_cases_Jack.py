import unittest
import pandas as pd
from basic_stock_stat import get_dates
from helper import check_ticker
from inspect_stock import inspect

class Tests(unittest.TestCase):

    def testStd_check_ticker(self):
        value = check_ticker("ROST", "Tests/DataForTesting/test_data_sample.csv")
        self.assertEqual(value, True)

    def testWrong_check_ticker(self):
        value = check_ticker("AMOR", "Tests/DataForTesting/test_data_sample.csv")
        self.assertEqual(value, False)

    def test_get_dates(self):
        values = get_dates("AMZN", "Data/Polished/NO_NULL_nasdaq_2010_mid_separate_year_month_day.csv")
        trueValues = ([2010, 1], [2022, 3])
        self.assertEqual(values, trueValues)
    
    def testWrong_get_dates(self):
        values = get_dates("AMZN", "Data/Polished/NO_NULL_nasdaq_2010_mid_separate_year_month_day.csv")
        trueValues = ([2009,2], [2021,5])
        self.assertFalse(values == trueValues)

    def test_inspect(self):

        testData = pd.read_csv("Tests/DataForTesting/test_data_sample.csv")
        # testData = pd.read_csv("Data/Polished/NO_NULL_nasdaq_2010_mid_separate_year_month_day.csv")
        testData["Date"] = pd.to_datetime(testData["Date"])

        value = inspect("ROST", [2020, 10], "Low", testData)
        trueValue = 94.87999725341795

        self.assertEqual(value, trueValue)
    
    def testWrong_inspect(self):
        """This tests if when an incorrect value is inputted whether it is recognized as being incorrect or not"""
        testData = pd.read_csv("Tests/DataForTesting/test_data_sample.csv")
        # testData = pd.read_csv("Data/Polished/NO_NULL_nasdaq_2010_mid_separate_year_month_day.csv")
        testData["Date"] = pd.to_datetime(testData["Date"])

        value = inspect("ROST", [2020, 10], "Low", testData)
        trueValue = 95

        self.assertFalse(value == trueValue)


if __name__ == '__main__':
    unittest.main()