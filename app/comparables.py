from pandas.io.parsers.readers import read_csv
import plotly.graph_objects as go

from app.alpha import get_symbol
from app.alpha import API_KEY
from app.overview import fetch_income_data
from app.overview import fetch_balance_data
from app.overview import calc_total_debt
from app.overview import calc_debt_ratio
from app.overview import calc_coverage_ratio
from app.overview import format_debt

industry_csv_url = 'https://github.com/jsh152/Debt_Metrics_Freestyle/raw/main/industries.csv'

industry_csv_data = read_csv(industry_csv_url)

symbol = get_symbol()

input_symbol = symbol.upper()

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

true_comp_symbols = [input_symbol]
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
comp_debt_symbols = []

comp_debt_metrics = {'Companies': comp_debt_symbols, 'TotalDebt': comp_total_debt,
'DebtRatio': comp_debt_ratio, 'CoverageRatio': comp_coverage_ratio }

for z in range(0,5):
    symbol = true_comp_symbols[z]
    try:
        income_data = fetch_income_data(symbol)
        balance_data = fetch_balance_data(symbol)
        total_debt = calc_total_debt(symbol, balance_data)
        formatted_debt = format_debt(symbol, balance_data, total_debt)
        debt_ratio = calc_debt_ratio(symbol, balance_data, total_debt)
        coverage_ratio = calc_coverage_ratio(symbol, income_data)

        comp_total_debt.append(formatted_debt)
        comp_debt_ratio.append(debt_ratio)
        comp_coverage_ratio.append(coverage_ratio)
        comp_debt_symbols.append(symbol)

    except:
        pass

total_num_comps = len(comp_debt_symbols)

comp_debt_table = go.Figure(data=[go.Table(
        header=dict(values=['Debt Metrics', 
        comp_debt_symbols[0],comp_debt_symbols[1],comp_debt_symbols[2],
        comp_debt_symbols[3]],
                    fill_color='navy', font=dict(color='white', size=12.25),
                    align='left'),
        cells=dict(values=[['Total Debt','Debt/Asset Ratio','Interest Coverage Ratio'],
            [comp_total_debt[0], comp_debt_ratio[0], comp_coverage_ratio[0]], 
            [comp_total_debt[1], comp_debt_ratio[1], comp_coverage_ratio[1]],
            [comp_total_debt[2], comp_debt_ratio[2], comp_coverage_ratio[2]],
            [comp_total_debt[3], comp_debt_ratio[3], comp_coverage_ratio[3]]],
                fill_color='lavender', font=dict(color='black', size=12),
                align='left'))
    ])
comp_debt_table.update_layout(title_text= 'Comparable Companies')

comp_debt_table.show()