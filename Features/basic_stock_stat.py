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
from helper import check_ticker, get_dataframe
from Features import helper

def get_dates_input():
    """
    Description:
        Main function for feature 2: basic stock stat. Takes in command line argument and calls helper 
        method get_dates() to retrieve the correct output.

    Input Signature: 
        1. ticker: command line argument specifying ticker symbol of stock

    Output:
        1. A list of two elements:
            - Ticker symbol
            - Another list contains the earliest and the latest date of the stock
    """
    ticker = str(sys.argv[2])
    fileName = "./Data/Polished/NO_NULL_nasdaq_2010_mid_separate_year_month_day.csv"
    output = get_dates(ticker, fileName)
    return output

#------------------------------

def get_nasdaqDates(ticker):
    """

    PENDING DELETION PENDING DELETION PENDING DELETION PENDING DELETION

    Desciption:
        Basic function which calls get_dates method with a preset fileName, which in this case is the NASDAQ dataset

    Input Signture:
        1. Ticker symbol of the stock you want dates for

    Output Signature:
        1. Returns the result of calling get_dates(ticker, fileName) when by default fileName is the NASDAQ dataset,
        essentially used when you know you want to call get_dates on the nasdaq set and want to avoid inputting an extra parameter.
    """
    fileName = "../Data/Polished/NO_NULL_nasdaq_2010_mid_separate_year_month_day.csv"
    get_dates(ticker, fileName)

#------------------------------

def get_dates(ticker, fileName):
    """
    Description:
        Read through our data file and find the earliest and latest 
        recorded dates of a particular stock by calling basic_stock_stat 
        helper method. 

    Input Signature:
        1. Ticker symbol
        2. fileName (the path to our the .csv file)

    Output Signature:
        1. Returns the earliest and latest recorded date of a stock (in a two-element list)

    """

    # sets variable to dataframe by calling helper function to avoid layer of abstraction
    nasdaq_df = get_dataframe(fileName)

    # calls helper function to check if ticker is in dataset
    if not check_ticker(ticker, fileName):
        return "Ticker not found in dataset"
   
    # outputs the list of earliest and latest dates and prints and returns it
    output = stock_extreme_dates(ticker, nasdaq_df)
    return output

#------------------------------

def stock_extreme_dates(ticker, dataframe):
    """
    Description:
        Find the earliest and latest record dates of a stock. Calls on a helper method 
        find_earliest_or_latest_record() to do this to avoid abstraction.

    Input Signature:
        1. ticker symbol (string)

    Output Signature:
        1. list [earliest year in record, earliest month in record]
        2. list [latest year in record, latest month in record]
    """

    # find the earliest dates
    earliest_date = find_earliest_or_latest_record(ticker, method = "earliest", dataframe = dataframe)

    # find the latest dates
    latest_date = find_earliest_or_latest_record(ticker, method = "latest", dataframe = dataframe)

    return earliest_date, latest_date

# ----------------------------

def find_earliest_or_latest_record(ticker, method, dataframe):
    """
    Description:
        Helper method to avoid any layers of abstraction. Takes in a parameter method that specifies
        earliest or latest dates. 

    Input Signature:
        ticker: ticker symbol of specified stock
        method: specifies if finding the earliest or latest dates of a stock
        dataframe: dataset of stocks

    Output:
        1. list [earliest year in record, earliest month in record]
        OR
        2. list [latest year in record, latest month in record]
        depending on 'method' parameter
    """

    if method == "earliest":

        # find the earliest year
        earliest_year = dataframe.loc[dataframe["Ticker Symbol"] == ticker]\
            ["Year"].min()

        # find the earliest month
        earliest_month = dataframe.loc[(dataframe["Ticker Symbol"] == ticker) &\
            (dataframe["Year"] == earliest_year)]\
            ["Month"].min()

        return [earliest_year, earliest_month]


    elif method == "latest":

        # find the latest year
        latest_year = dataframe.loc[dataframe["Ticker Symbol"] == ticker]\
            ["Year"].max()

        # find the latest month
        latest_month = dataframe.loc[(dataframe["Ticker Symbol"] == ticker) &\
            (dataframe["Year"] == latest_year)]\
            ["Month"].max()

        return [latest_year, latest_month]

if __name__ == '__main__':
    get_dates_input()