import plotly.graph_objects as go

from app.alpha import get_symbol
from app.alpha import API_KEY
from app.overview import fetch_balance_data
from app.overview import fetch_income_data
from app.debt_graphs import calc_debt_metrics

symbol = get_symbol()
balance_sheet_data = fetch_balance_data(symbol)
income_sheet_data = fetch_income_data(symbol)

num_years = len(balance_sheet_data['annualReports'])

debt_series = []
debt_ratios = []
coverage_ratios = []
reported_dates = []
form_debt_series = []
form_debt_ratios = []
form_coverage_ratios = []

debt_metrics = {'totaldebt': debt_series, 'debtratio': debt_ratios, 'coverageratio': coverage_ratios, 'dates': reported_dates}
formatted_debt_metrics = {'totaldebt': form_debt_series, 'debtratio': form_debt_ratios, 'coverageratio': form_coverage_ratios, 'dates': reported_dates}


total_debt_metrics = calc_debt_metrics(num_years, balance_sheet_data, income_sheet_data, 
debt_series, debt_ratios, coverage_ratios, reported_dates,
form_debt_series, form_debt_ratios, form_coverage_ratios, debt_metrics,
formatted_debt_metrics)

debt_table = go.Figure(data=[go.Table(
    header=dict(values=['total_debt_metrics',debt_metrics['dates'][0],debt_metrics['dates'][1],debt_metrics['dates'][2],debt_metrics['dates'][3],debt_metrics['dates'][4]],
                fill_color='navy', font=dict(color='white', size=12.25),
                align='left'),
    cells=dict(values=[['Total Debt','Debt/Asset Ratio','Interest Coverage Ratio'],[formatted_debt_metrics['totaldebt'][0],formatted_debt_metrics['debtratio'][0],
                    formatted_debt_metrics['coverageratio'][0]],[formatted_debt_metrics['totaldebt'][1],formatted_debt_metrics['debtratio'][1],
                    formatted_debt_metrics['coverageratio'][1]],[formatted_debt_metrics['totaldebt'][2],formatted_debt_metrics['debtratio'][2],
                    formatted_debt_metrics['coverageratio'][2]],[formatted_debt_metrics['totaldebt'][3],formatted_debt_metrics['debtratio'][3],
                    formatted_debt_metrics['coverageratio'][3]],[formatted_debt_metrics['totaldebt'][4],formatted_debt_metrics['debtratio'][4],
                    formatted_debt_metrics['coverageratio'][4]]],
               fill_color='lavender', font=dict(color='black', size=12),
               align='left'))
])
debt_table.show()
