#This is the overview file. Here, basic debt metrics will be presented abou the company at a glance


import requests
import json
from app.alpha import get_symbol
from app.alpha import API_KEY

def fetch_balance_data(symbol):
    
    balance_url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={API_KEY}"

    raw_balance_data = requests.get(balance_url)

    parsed_balance_data = json.loads(raw_balance_data.text)

    return parsed_balance_data


def fetch_income_data(symbol):

    income_url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={API_KEY}"

    raw_income_data = requests.get(income_url)

    parsed_income_data = json.loads(raw_income_data.text)

    return parsed_income_data

def calc_total_debt(symbol, balance_data):

    if balance_data['annualReports'][0]['shortTermDebt'] == 'None':
        shortterm_debt = 0.0
    else:
        shortterm_debt = float(balance_data['annualReports'][0]['shortTermDebt'])

    if balance_data['annualReports'][0]['longTermDebtNoncurrent'] == 'None':
        longterm_debt = 0.0
    else:
        longterm_debt = float(balance_data['annualReports'][0]['longTermDebtNoncurrent'])

    total_debt_amt = shortterm_debt + longterm_debt

    return total_debt_amt

def calc_debt_ratio(symbol, balance_data, total_debt):
    total_debt = calc_total_debt(symbol, balance_data)
    
    balance_data = fetch_balance_data(symbol)

    total_assets = float(balance_data['annualReports'][0]['totalAssets'])

    debt_asset_ratio = total_debt / total_assets

    return debt_asset_ratio

def calc_coverage_ratio(symbol,income_data ):
    EBIT = float(income_data['annualReports'][0]['ebit'])

    if income_data['annualReports'][0]['interestExpense'] == 'None':
        interest_expense = 0.0
    else:
        interest_expense = float(income_data['annualReports'][0]['interestExpense'])

    int_coverage_ratio = EBIT / interest_expense

    return int_coverage_ratio


if __name__ == "__main__":
    try:
        symbol = get_symbol()
        income_data = fetch_income_data(symbol)
        balance_data = fetch_balance_data(symbol)
        total_debt = calc_total_debt(symbol, balance_data)
        debt_ratio = calc_debt_ratio(symbol, balance_data, total_debt)
        coverage_ratio = calc_coverage_ratio(symbol, income_data)

        statements_date = balance_data['annualReports'][0]['fiscalDateEnding']

        print('')

        print("As of " + statements_date + " " + symbol + " has:")

        print("")

        print("Total debt of: $" + str(total_debt / 1000000000) + " billion.")

        formatted_debt_ratio = "{:.2f}".format(debt_ratio)

        print("A debt/asset ratio of: " + formatted_debt_ratio)

        formatted_coverage_ratio = "{:.2f}".format(coverage_ratio)

        print("An interest coverage ratio of: " + formatted_coverage_ratio)
    
    except:
        print("We couldn't find that symbol. Please try again with a valid symbol and API Key.")