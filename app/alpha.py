#This is the alpha file. Get the api key

import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_symbol():
    stock_symbol = input("Please enter the ticker symbol of the business that you would like to analyze: ")
    return stock_symbol

