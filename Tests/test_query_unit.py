import sys
sys.dont_write_bytecode = True

import pandas as pd
import unittest
import sys
sys.path.append('../H/Features')
from inspect_stock import *

class TestInspectCaseVolume(unittest.TestCase):
    def test_case_(self):
        """
        Tests that right volume is returned when inputted correct values to find_query function

        Uses dummy data in Tests/DataForTesting/test_data_sample.csv to check function
        """
        sample_df = pd.read_csv("Tests/DataForTesting/test_data_sample.csv")

        output = find_query(6, "SAFM", 2017, 9, "Volume", "Tests/DataForTesting/test_data_sample.csv", sample_df)
        actual = 669900.0
        self.assertEqual(float(output), actual)

class TestInspectCaseLow(unittest.TestCase):
    def test_case_(self):
        """
        Tests that right open is returned when inputted correct values to find_query function

        Uses dummy data in Tests/DataForTesting/test_data_sample.csv to check function
        """
        sample_df = pd.read_csv("Tests/DataForTesting/test_data_sample.csv")

        output = find_query(6, "HWBK", 2012, 2, "Low", "Tests/DataForTesting/test_data_sample.csv", sample_df)
        actual = 6.57344389
        self.assertEqual(float(output), actual)

class TestInspectCaseHigh(unittest.TestCase):
    def test_case_(self):
        """
        Tests that right high is returned when inputted correct values to find_query function

        Uses dummy data in Tests/DataForTesting/test_data_sample.csv to check function
        """
        sample_df = pd.read_csv("Tests/DataForTesting/test_data_sample.csv")

        output = find_query(6, "ROST", 2020, 10, "High", "Tests/DataForTesting/test_data_sample.csv", sample_df)
        actual = 96.94000244
        self.assertEqual(float(output), actual)

class TestInspectCaseClose(unittest.TestCase):
    def test_case_(self):
        """
        Tests that right close is returned when inputted correct values to find_query function

        Uses dummy data in Tests/DataForTesting/test_data_sample.csv to check function
        """
        sample_df = pd.read_csv("Tests/DataForTesting/test_data_sample.csv")

        output = find_query(6, "EQIX", 2014, 12, "Close", "Tests/DataForTesting/test_data_sample.csv", sample_df)
        actual = 221.8600006
        self.assertEqual(float(output), actual)

class TestInspectCaseOpen(unittest.TestCase):
    def test_case_(self):
        """
        Tests that right open is returned when inputted correct values to find_query function

        Uses dummy data in Tests/DataForTesting/test_data_sample.csv to check function
        """
        sample_df = pd.read_csv("Tests/DataForTesting/test_data_sample.csv")

        output = find_query(6, "USLM", 2019, 3, "Open", "Tests/DataForTesting/test_data_sample.csv", sample_df)
        actual = 74.56999969
        self.assertEqual(float(output), actual)

if __name__ == '__main__':
    unittest.main()