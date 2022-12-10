#This is the alpha file. Get the api key and stock symbol from user


#from getpass import getpass

def get_API():
    from getpass import getpass
    API_KEY = getpass("Please input your AlphaVantage API Key: ") 

def get_symbol():
    stock_symbol = input("Please enter the ticker symbol of the business that you would like to analyze.")


