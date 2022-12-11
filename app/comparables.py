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

comp_symbols = []
comp_values_diff = []
comp_industry = []
comp_marketcap = []
comparable_companies = {'Symbols': comp_symbols, 'MarketCapDiff': comp_values_diff, 'Industry': comp_industry, 'MarketCap': comp_marketcap}
true_comp_symbols = []
true_comp_values = []
true_comps = {'Symbols': true_comp_symbols, 'MarketCap': true_comp_values}
comp_total_debt = []
comp_debt_ratio = []
comp_coverage_ratio = []
comp_debt_symbols = []
comp_debt_metrics = {'Companies': comp_debt_symbols, 'TotalDebt': comp_total_debt,
'DebtRatio': comp_debt_ratio, 'CoverageRatio': comp_coverage_ratio }


#I have the list of industries and listed stocks stored in a csv file, this function accesses that data
def get_csv_url():
    industry_csv_url = 'https://github.com/jsh152/Debt_Metrics_Freestyle/raw/main/industries.csv'

    csv_data = read_csv(industry_csv_url)

    return csv_data

#Create a dictionary filled with all of the companies in the selected company's industry and the difference in value between
#each and the selected company
def get_industry_companies(num_stocks, industry_csv_data, stock_industry, comp_symbols, comp_industry, comp_marketcap, comp_values_diff, comparable_companies):
    for j in range(0,num_stocks):
        if industry_csv_data['Industry'][j] == stock_industry:
            comp_symbols.append(industry_csv_data['Symbol'][j])
            comp_industry.append(industry_csv_data['Industry'][j])
            comp_marketcap.append(industry_csv_data['Market Cap'][j])

            value_diff = abs(float(industry_csv_data['Market Cap'][k_value]) - float(industry_csv_data['Market Cap'][j]))
            comp_values_diff.append(value_diff)
    return comparable_companies

#Create a dictionary containing the 4 competitors with market caps closest to the selected company
def get_comparable_companies(num_series_stock, num_comparables, comparable_companies, dupl_comp_values_diff, true_comps):
    for m in range(num_series_stock,num_series_stock + 5):
        for l in range(0,num_comparables):
            if comparable_companies['MarketCapDiff'][l] == dupl_comp_values_diff[m]:
                true_comp_symbols.append(comparable_companies['Symbols'][l])
                true_comp_values.append(comparable_companies['MarketCap'][l])
    return true_comps

#Create a dictionary containing all relevant debt metrics for each comparable company
def get_comps_metrics(true_comp_symbols, comp_debt_metrics):
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
    return comp_debt_metrics

#Now that we have a dictionary containing comparable companies and all debt metrics, all that's left to do is create the table
def create_comps_table(comparable_metrics, comp_debt_symbols, comp_total_debt, comp_debt_ratio, comp_coverage_ratio):
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
    return comp_debt_table

if __name__ == "__main__":    
    try:
        industry_csv_data = get_csv_url()
        symbol = get_symbol()

        num_stocks = len(industry_csv_data)

        #Search the industry CSV file to find the industry that the user inputted stock is in
        for k in range(0,num_stocks):
            if industry_csv_data['Symbol'][k].upper() == symbol.upper():
                stock_industry = industry_csv_data['Industry'][k]
                k_value = k

        industry_participants = get_industry_companies(num_stocks, industry_csv_data, stock_industry, comp_symbols, comp_industry, comp_marketcap, comp_values_diff, comparable_companies)
        print(type(industry_participants))
        #Determine if the selected company has multiple series of publicly traded shares
        num_series_stock = comp_values_diff.count(0.0)

        #Create a copy of the list containing the differences between the marketcap of the selected company and competitors to sort without changing original
        dupl_comp_values_diff = comp_values_diff.copy()

        #Sort the list containing the differences in market cap so that the smallest differences are at the start of the list
        dupl_comp_values_diff.sort(key=abs)

        #Number of companies in the same industry
        num_comparables = len(comp_symbols)

        input_symbol = symbol.upper()

        #Declare lists included in the final dictionary. Have the first entry of the comparable companies list be the selected company
        true_comp_symbols = [input_symbol]
        
        true_comparables = get_comparable_companies(num_series_stock, num_comparables, comparable_companies, dupl_comp_values_diff, true_comps)

        comparable_metrics = get_comps_metrics(true_comp_symbols, comp_debt_metrics)

        comparable_table = create_comps_table(comparable_metrics, comp_debt_symbols, comp_total_debt, comp_debt_ratio, comp_coverage_ratio)

        comparable_table.show()
    except:
        print("We couldn't find that symbol. Please try again with a valid symbol and API Key.")
