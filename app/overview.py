#This is the overview file. Here, basic debt metrics will be presented abou the company at a glance

#from app.alpha import get_API
#from app.alpha import get_symbol

#get_API()

#get_symbol()

from getpass import getpass
API_KEY = getpass("Please input your AlphaVantage API Key: ") 

stock_symbol = input("Please enter the ticker symbol of the business that you would like to analyze.")

balance_url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={stock_symbol}&apikey={API_KEY}"

raw_balance_data = requests.get(balance_url)

parsed_balance_data = json.loads(raw_balance_data.text)

statements_date = parsed_balance_data['annualReports'][0]['fiscalDateEnding']

shortterm_debt = float(parsed_balance_data['annualReports'][0]['shortTermDebt'])

longterm_debt = float(parsed_balance_data['annualReports'][0]['longTermDebtNoncurrent'])

total_debt = shortterm_debt + longterm_debt


print("As of " + statements_date + " " + stock_symbol + " has:")

print("")

print("Total debt of: $" + str(total_debt / 1000000000) + " billion.")

total_assets = float(parsed_balance_data['annualReports'][0]['totalAssets'])

debt_ratio = total_debt / total_assets

formatted_debt_ratio = "{:.2f}".format(debt_ratio)

print("A debt/asset ratio of: " + formatted_debt_ratio)



income_url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={stock_symbol}&apikey={API_KEY}"

raw_income_data = requests.get(income_url)

parsed_income_data = json.loads(raw_income_data.text)

EBIT = float(parsed_income_data['annualReports'][0]['ebit'])

interest_expense = float(parsed_income_data['annualReports'][0]['interestExpense'])

coverage_ratio = EBIT / interest_expense

formatted_coverage_ratio = "{:.2f}".format(coverage_ratio)

print("An interest coverage ratio of: " + formatted_coverage_ratio)