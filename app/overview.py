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

if __name__ == "__main__":
    symbol = get_symbol()

    balance_data = fetch_balance_data(symbol)

    income_data = fetch_income_data(symbol)

    statements_date = balance_data['annualReports'][0]['fiscalDateEnding']

    shortterm_debt = float(balance_data['annualReports'][0]['shortTermDebt'])

    longterm_debt = float(balance_data['annualReports'][0]['longTermDebtNoncurrent'])

    total_debt = shortterm_debt + longterm_debt

    print("As of " + statements_date + " " + symbol + " has:")

    print("")

    print("Total debt of: $" + str(total_debt / 1000000000) + " billion.")

    total_assets = float(balance_data['annualReports'][0]['totalAssets'])

    debt_ratio = total_debt / total_assets

    formatted_debt_ratio = "{:.2f}".format(debt_ratio)

    print("A debt/asset ratio of: " + formatted_debt_ratio)

    EBIT = float(income_data['annualReports'][0]['ebit'])

    interest_expense = float(income_data['annualReports'][0]['interestExpense'])

    coverage_ratio = EBIT / interest_expense

    formatted_coverage_ratio = "{:.2f}".format(coverage_ratio)

    print("An interest coverage ratio of: " + formatted_coverage_ratio)
