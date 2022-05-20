# WE ARE NOT USING THIS SHIT

# Pycache are evil, don't produce them
import sys
sys.dont_write_bytecode = True

import flask
import pandas as pd

import sys
sys.path.append('Features')
from inspect_stock import *
from basic_stock_stat import *
from stock_ROI import *
from helper import *

app = flask.Flask(__name__)

#------------------------------

# read in pandas dataframe
nasdaq_df = get_dataframe()

#------------------------------

@app.route("/")
def homepage():
    """
    DESCRIPTION:
        Create a homepage for the beta website.
    INPUT SIGNATURE:
        1. None, this is the home page.
    OUTPUT SIGNATURE:
        1. Render the home page from our html template
    """

    header = "INVEST.ED BETA PLATFORM"
    home = "From here, you can navigate using the following routes to use the corresponding functions\n\n\
            1. Inspect a stock\n\
                * Route: /inspect_stock/[ticker symbol]/[year]/[month]/[statistic]\n\
                * Example: /inspect_stock/AAPL/2022/3/Open\n\n\
            2. Find the earliest and latest recorded dates of a stock in our database\n\
                * Route: /extreme_dates/[ticker symbol]\n\
                * Example: /extreme_dates/MSFT\n\n\
            3. Find the ROI of any stock (in percentage)\n\
                * Route: /stock_ROI/[ticker symbol]/[investment year]/[investment month]/[buying price]\
                    /[divestment year]/[divestment month]/[selling price]\n\
                * Example: /stock_ROI/AMZN/2011/12/Low/2022/3/High\n"

    home2 = home.replace('\n', '<br>')

    return flask.render_template('invested_beta_template.html',\
        header1 = header,\
        title = "Invest.Ed Beta Platform",\
        text1 = home2)

#------------------------------

@app.route("/stock_ROI/<ticker_symbol>/<investment_year>/<investment_month>/<buying_price>/<divestment_year>/<divestment_month>/<selling_price>")
def flask_stock_ROI(ticker_symbol, investment_year, investment_month, buying_price,\
    divestment_year, divestment_month, selling_price):
    """
    DESCRIPTION:
        This function is the web-interface of our stock_ROI feature.
        It displays to the user what is their return on investment in percentage value.
    
    INPUT SIGNATURE:
        1. ticker_symbol: the ticker of the stock of interest
        2. investment_year: the year that the hypothetical investment was made
        3. investment_month: the month that the hypothetical investment was made
        4. buying_price: the price the stock was invested at, choose between 'Open', 'Close', 'Low', 'High', and 'Adjusted Close'
        5. divestment_year: the year that the hypothetical divestment was made
        6. divestment_month: the month that the hypothetical divestment was made
        7. selling_price: the price the stock was divested at, choose between 'Open', 'Close', 'Low', 'High', and 'Adjusted Close'

    OUTPUT SIGNATURE:
        1. message_stock_ROI (string): a message conveying the ROI of the chosen stock
    """

    # convert input into the appropriate data format
    investment_year = int(investment_year)
    investment_month = int(investment_month)
    divestment_year = int(divestment_year)
    divestment_month = int(divestment_month)

    # convert the date variables into the appropriate data structure
    date_invest = [investment_year, investment_month]
    date_divest = [divestment_year, divestment_month]

    # calculate the ROI
    ROI = main_stock_ROI(ticker_symbol, date_invest, date_divest, buying_price, selling_price)

    # if there is no error
    if isinstance(ROI, float) == True:

        # message to display
        message_stock_ROI = "You invested in " + ticker_symbol +\
            "\nfrom " + str(investment_year) + "/" + str(investment_month) + " at " + buying_price +\
            "\nto " + str(divestment_year) + "/" + str(divestment_month) + " at " + selling_price +\
            "\n\n" +\
            "Your ROI (%): " + str(ROI)

        # convert message to html-friendly format
        message_stock_ROI = message_stock_ROI.replace("\n", "<br>")

    # we encountered an error
    else:

        # pass on the error
        message_stock_ROI = ROI

    return message_stock_ROI

#------------------------------

@app.route('/extreme_dates/<ticker>', strict_slashes=False)
def get_dates_of_stock(ticker):
    """
    DESCRIPTION:
        Call upon the basic_stock_stat.py file within the back end and find the earliest and latest dates of a stock in the data

    INPUT SIGNATURE:
        1. ticker (string): the ticker of the interested stock

    OUTPUT SIGNATURE:
        1. result (string): a string contains the earliest and latest dates in the data of said stock
            If there is any error, the string returned from the back_end will change to reflect that error itself
    """
    
    if not check_ticker(str(ticker)):
        return str(get_dates(str(ticker)))
        # return page_not_found(not check_ticker(str(ticker), "./Data/Polished/NO_NULL_nasdaq_2010_mid_separate_year_month_day.csv"))"
    result = str(get_dates(str(ticker)))
    return "The dates for " + str(ticker) + " are " + result

#------------------------------

@app.route('/inspect_stock/<ticker>/<year>/<month>/<query_stat>', strict_slashes=False)
def inspect_specifified_stock(ticker,year,month,query_stat):
    """
    Description: 
        Shows the user a stock statistic based on input stock information or returns an invalid input message for invalid inputs
    Parameters:
        ticker - stock ticker for the stock intending to inspect
        year - year for inspecting the stock between 2001 and 2022 inclusive
        month - month for inspecting the stock between 1 and 12 inclusive
        query_stat - the stat of the stock to inspect including open, close, low, and high
    Returns:
        description - A string description of the stock/stat and the desired value in the format: (ticker)'s (query_stat) on (month)/(year): 
        value - A string that is the desired value follows immediately after the desciption
    
    """
    value = find_query(6, str(ticker), int(year), int(month), str(query_stat), nasdaq_df)
    description = ""
    if not isinstance(value,str) :
        #checks to see if output is not an invalid input message
        description = str(ticker) + "'s " + str(query_stat) + " on " + str(month) + "/" + str(year) + ": "
    return description + str(value)

#------------------------------

@app.errorhandler(404)
def page_not_found(e):
    """
        Description:
            A page to instruct the user on the steps to follow if an invalid route is entered.
        Returns:
            1. message404 - a string conveying further instructions to the user
    """

    # the message to be displayed
    message404 = "ERROR 404\n\nInvalid Route.\
        \nReturn to Home Page for more instruction. (i.e. You can use the Back button.)\n\n\
        This might be due to some of the following reasons:\n\n\
            1. You might have forgotten to specify the feature before you inputted the stock information.\n\n\
            2. You might have made a typo typing out the URL.\n\n\
            3. You might have not capitalized a query input or the ticker symbol.\n\n\
            4. Refer to these examples of the possible features to double check your URL\n\
            -----Feature Inspect Example: /inspect_stock/AAPL/2022/3/Open\n\
            -----Feature Extreme Dates Example: /extreme_dates/MSFT\n\
            -----Feature Stock ROI Example: /stock_ROI/AMZN/2011/12/Low/2022/3/High"

    # convert the message to html-friendly format
    message404 = message404.replace('\n', '<br>')

    # return the message
    return message404

#------------------------------

@app.errorhandler(500)
def python_bug(e):
    """
    Description:
        A page notifying the user that the encountered error is from the server, not the user.
    Returns:
        message500 -    a string informing the user that the error is from the server and it is not
                        their fault and tells them to inform the developement team 
    """

    # the message to be displayed
    message500 =  "ERROR 500: INTERNAL SERVER ERROR\n\nDon't panic, it's NOT your fault!\n\
    The error is on the server's end. Please report it to the administrator for a patch.\n\n\
    We thank you kindly,\n\
    Invest.Ed Development Team"

    # convert the message to html-friendly format
    message500 = message500.replace("\n", "<br>")

    # return the message
    return message500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 2727)