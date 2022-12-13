import plotly.express as px
import requests
import json

from app.alpha import get_symbol
from app.alpha import API_KEY
from app.overview import fetch_balance_data
from app.overview import fetch_income_data

debt_series = []
debt_ratios = []
coverage_ratios = []
reported_dates = []
form_debt_series = []
form_debt_ratios = []
form_coverage_ratios = []
debt_metrics = {'totaldebt': debt_series, 'debtratio': debt_ratios, 'coverageratio': coverage_ratios, 'dates': reported_dates}
formatted_debt_metrics = {'totaldebt': form_debt_series, 'debtratio': form_debt_ratios, 'coverageratio': form_coverage_ratios, 'dates': reported_dates}

def calc_debt_metrics(symbol, num_years, balance_sheet_data, income_sheet_data, 
debt_series, debt_ratios, coverage_ratios, reported_dates,
form_debt_series, form_debt_ratios, form_coverage_ratios, debt_metrics):
    for i in range(0, num_years):
        if balance_sheet_data['annualReports'][i]['shortTermDebt'] == 'None':
            shortterm_debt = 0.0
        else:
            shortterm_debt = float(balance_sheet_data['annualReports'][i]['shortTermDebt'])

        if balance_sheet_data['annualReports'][i]['longTermDebtNoncurrent'] == 'None':
            longterm_debt = 0.0
        else:
            longterm_debt = float(balance_sheet_data['annualReports'][i]['longTermDebtNoncurrent'])

        total_debt = (shortterm_debt + longterm_debt)

        form_total_debt = str(round((total_debt / 1000000000), ndigits= 2)) + ' Billion'

        debt_series.append(total_debt)

        form_debt_series.append(form_total_debt)

        total_assets = float(balance_sheet_data['annualReports'][i]['totalAssets'])

        debt_ratio = total_debt / total_assets

        form_debt_ratio = round(debt_ratio, ndigits= 2)

        debt_ratios.append(debt_ratio)

        form_debt_ratios.append(form_debt_ratio)

        EBIT = float(income_sheet_data['annualReports'][i]['ebit'])

        if income_sheet_data['annualReports'][i]['interestExpense'] == 'None':
            interest_expense = 0.0
        else:
            interest_expense = float(income_sheet_data['annualReports'][i]['interestExpense'])

        coverage_ratio = EBIT / interest_expense

        form_coverage_ratio = round(coverage_ratio, ndigits= 2)

        coverage_ratios.append(coverage_ratio)

        form_coverage_ratios.append(form_coverage_ratio)

        statements_date = balance_sheet_data['annualReports'][i]['fiscalDateEnding']

        reported_dates.append(statements_date)

    return debt_metrics

if __name__ == "__main__":
    try:
        symbol = get_symbol()
        balance_sheet_data = fetch_balance_data(symbol)
        income_sheet_data = fetch_income_data(symbol)

        num_years = len(balance_sheet_data['annualReports'])

        total_debt_metrics = calc_debt_metrics(symbol, num_years, balance_sheet_data, income_sheet_data, 
        debt_series, debt_ratios, coverage_ratios, reported_dates,
        form_debt_series, form_debt_ratios, form_coverage_ratios, debt_metrics)

        debt_fig = px.line(total_debt_metrics, x='dates', y='totaldebt', labels={'dates': "Date", 'totaldebt': "Total Debt"})

        debt_fig.update_layout(title_text= symbol.upper())

        debt_fig.show()

        debtratio_fig = px.line(total_debt_metrics, x='dates', y='debtratio', labels={'dates': "Date", 'debtratio': "Debt/Asset Ratio"})

        debtratio_fig.update_layout(title_text= symbol.upper())

        debtratio_fig.show()

        interestcov_fig = px.line(total_debt_metrics, x='dates', y='coverageratio', labels={'dates': "Date", 'coverageratio': "Interest Coverage Ratio"})

        interestcov_fig.update_layout(title_text= symbol.upper())

        interestcov_fig.show()
    except:
        print("We couldn't find that symbol. Please try again with a valid symbol and API Key.")
