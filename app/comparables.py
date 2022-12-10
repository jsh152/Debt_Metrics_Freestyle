from pandas.io.parsers.readers import read_csv

from app.alpha import get_symbol
from app.alpha import API_KEY

industry_csv_url = 'https://github.com/jsh152/Debt_Metrics_Freestyle/raw/main/industries.csv'

industry_csv_data = read_csv(industry_csv_url)

symbol = get_symbol()

num_stocks = len(industry_csv_data)

for k in range(0,num_stocks):
    if industry_csv_data['Symbol'][k].upper() == symbol.upper():
        stock_industry = industry_csv_data['Industry'][k]
        k_value = k

comp_symbols = []
comp_values_diff = []
comp_industry = []
comparable_companies = {'Symbols': comp_symbols, 'MarketCap': comp_values_diff,
'Industry': comp_industry}

for j in range(0,num_stocks):
    if industry_csv_data['Industry'][j] == stock_industry:
        comp_symbols.append(industry_csv_data['Symbol'][j])
        comp_industry.append(industry_csv_data['Industry'][j])

        value_diff = abs(float(industry_csv_data['Market Cap'][k_value]) - float(industry_csv_data['Market Cap'][j]))
        comp_values_diff.append(value_diff)

print(comparable_companies)