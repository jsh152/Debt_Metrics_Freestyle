from pandas.io.parsers.readers import read_csv

from app.alpha import get_symbol
from app.alpha import API_KEY
from app.overview import fetch_income_data
from app.overview import fetch_balance_data
from app.overview import calc_total_debt
from app.overview import calc_debt_ratio
from app.overview import calc_coverage_ratio

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
comp_marketcap = []
comparable_companies = {'Symbols': comp_symbols, 'MarketCapDiff': comp_values_diff,
'Industry': comp_industry, 'MarketCap': comp_marketcap}

for j in range(0,num_stocks):
    if industry_csv_data['Industry'][j] == stock_industry:
        comp_symbols.append(industry_csv_data['Symbol'][j])
        comp_industry.append(industry_csv_data['Industry'][j])
        comp_marketcap.append(industry_csv_data['Market Cap'][j])

        value_diff = abs(float(industry_csv_data['Market Cap'][k_value]) - float(industry_csv_data['Market Cap'][j]))
        comp_values_diff.append(value_diff)

num_series_stock = comp_values_diff.count(0.0)

dupl_comp_values_diff = comp_values_diff.copy()

dupl_comp_values_diff.sort(key=abs)

num_comparables = len(comp_symbols)

true_comp_symbols = []
true_comp_values = []

true_comps = {'Symbols': true_comp_symbols, 'MarketCap': true_comp_values,
'Industry': [comp_industry[0], comp_industry[1], comp_industry[2], comp_industry[3], comp_industry[4]]}

for m in range(num_series_stock,num_series_stock + 5):
    for l in range(0,num_comparables):
        if comparable_companies['MarketCapDiff'][l] == dupl_comp_values_diff[m]:
            true_comp_symbols.append(comparable_companies['Symbols'][l])
            true_comp_values.append(comparable_companies['MarketCap'][l])


comp_total_debt = []
comp_debt_ratio = []
comp_coverage_ratio = []

comp_debt_metrics = {'Companies': true_comp_symbols, 'TotalDebt': comp_total_debt,
'DebtRatio': comp_debt_ratio, 'CoverageRatio': comp_coverage_ratio }

for z in range(0,5):
    symbol = true_comp_symbols[z]
    try:
        income_data = fetch_income_data(symbol)
        balance_data = fetch_balance_data(symbol)
        total_debt = calc_total_debt(symbol, balance_data)
        debt_ratio = calc_debt_ratio(symbol, balance_data, total_debt)
        coverage_ratio = calc_coverage_ratio(symbol, income_data)

        comp_total_debt.append(total_debt)
        comp_debt_ratio.append(debt_ratio)
        comp_coverage_ratio.append(coverage_ratio)

    except:
        pass

print(comp_debt_metrics)