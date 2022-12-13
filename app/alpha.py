#This is the alpha file. Get the api key

import os
from dotenv import load_dotenv

#Load in the API Key from the .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")

#Function that asks user to input stock symbol of company they want to analyze
def get_symbol():
    stock_symbol = input("Please enter the ticker symbol of the business that you would like to analyze: ")
    return stock_symbol

