# Pycache are evil, don't produce them
import sys
sys.dont_write_bytecode = True

import path
# current directory
directory = path.Path(__file__).abspath()
# setting path to the directory with the feature
sys.path.append(directory.parent.parent)

from fileinput import filename
import sys
import csv
import pandas as pd
import datetime
from helper import check_ticker

def find_query_input():
    """
    Objective:
    This function is the main function for feature 1 of our command line interface, inspect stock. 

    Input Signature:
    ticker: this is the ticker symbol for the stock, ex. AAPL
    year: this is the specified year of the stock that the user wants to find, ex. 2021
    month: this is the specified month of the stock that the user wants to find, ex. 3
    query: This is the type of statistic that the user wants, ex. Open

    Output:
    The statistic (specified by the query input argument) of a stock (specified by ticker symbol)
    at a certain point in time (specified by month and year of investment).

    """

    # calls a helper method for reading file so ensures there is only 1 level of abstraction
    nasdaq_df = get_fileName()


    num_of_args = len(sys.argv)
    # assigns command line arguments to variables with correct types by casting
    if not check_num_args(num_of_args):
        print("There needs to be 4 arguments; TickerSymbol, Year, Month, Query")
        return 

    ticker = str(sys.argv[1])
    year = int(sys.argv[2])
    month = int(sys.argv[3])
    query = str(sys.argv[4])

    # calls find_query function to get the actual statistic and print and return the result
    output = find_query(num_of_args, ticker, year, month, query, "../Data/Polished/NO_NULL_nasdaq_2010_mid_separate_year_month_day.csv", nasdaq_df)
    print(output)
    return output

def get_fileName():
    """
    Objective:
    Helper function for reading the dataset to avoid multiple layers of abstraction

    Output: 
    Dataset ready for use in command line functions

    """
    nasdaq_df = pd.read_csv("../Data/Polished/NO_NULL_nasdaq_2010_mid_separate_year_month_day.csv")
    nasdaq_df["Date"] = pd.to_datetime(nasdaq_df["Date"])
    return nasdaq_df


def find_query(num_of_args, ticker, year, month, query, fileName, dataframe):
    """
    Objective:
    This function runs helper functions to check for the correct user input, including the 
    number of parameters and if the ticker symbol and date are in the dataset.

    Input Signature:
    Num_of_args: The number of arguments of the command line
    year: this is the specified year of the stock that the user wants to find, ex. 2021
    month: this is the specified month of the stock that the user wants to find, ex. 3
    query: This is the type of statistic that the user wants, ex. Open
    fileName: path of dataset to read
    dataframe: the dataset returned from get_fileName()

    """

    # checks if command line arguments are the correct number
    if not check_num_args(num_of_args):
        return "There needs to be 4 arguments; TickerSymbol, Year, Month, Query"

    # checks if ticker symbol is in the dataset and returns error statement if not found
    if not check_ticker(ticker, fileName):
        return "Ticker not found in dataset"

    # checks if the inputted date is in dataset and returns error statement if not found
    if not check_date(ticker, year, month, fileName):
        return "Invalid Date"
        
    # structures year and month into a list
    date = [year, month]

    # calls inspect function which finds the statistic and returns statistic
    output = inspect(ticker, date, query, dataframe)
    return output

def check_num_args(num_of_args):
    """
    This helper method insures there is the proper number of command line arugments". Returns true if there are 
    5 command line arugments and false if there is not exactly 5.
    """
    if num_of_args != 5:
        return False
    return True
    

def check_date(ticker, year, month, fileName):
    """
    This helper method checks to make sure that the specified date (year and month) is located within the dataset 
    for the specified ticker symbol. Returns true if it is found and false if it is not.
    """
    f = open(fileName, 'r', encoding = "UTF-8")
    with f as rFile:
        spamreader = csv.reader(rFile, delimiter=',')
        next(spamreader)
        for row in spamreader:
            if row[10] == ticker and row[3] == str(year) and row[2] == str(month):
                f.close
                return True
    f.close
    return False

def check_query(query):
    """
    This helper method checks whether the parameter query is valid and contained in our dataset. 
    Returns true if valid and false if invalid.
    """
    list = ["Low", "Open", "Volume", "High", "Close", "Adjusted Close"]
    if query in list:
        return True
    return False

def inspect(ticker, date, query_stat, dataframe):
    """
    Objective:
        1. Return the requested query statistic of a stock for a specific date from the 
        dataset

    Input Signature:
        1. ticker symbol of stock (string)
        2. year of investment (int64)
        3. month of investment (int64)
        4. query_stat (string, "Low", "Open", "Volume" "High", "Close", "Adjusted Close")

    Output Signature
        1. The relevant metric (query_stat) of a stock (ticker symbol) at a certain point in time (month and year of investment)
    """

    # locate the row that has the correct ticker and date value within our data
    row_of_interst = dataframe.loc[(dataframe['Ticker Symbol'] == ticker) & (dataframe['Year'] == date[0]) & (dataframe['Month'] == date[1])]

    # return the value at the column that is the requested query stat
    return row_of_interst.iloc[0][query_stat]

# main function to run find_query_input()
if __name__ == '__main__':
    find_query_input()