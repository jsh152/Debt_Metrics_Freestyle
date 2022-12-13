import plotly.graph_objects as go

from app.alpha import get_symbol
from app.alpha import API_KEY
from app.overview import fetch_balance_data
from app.overview import fetch_income_data
from app.debt_graphs import calc_debt_metrics

from app.debt_graphs import debt_series, debt_ratios, coverage_ratios, reported_dates, form_debt_series, form_debt_ratios, form_coverage_ratios 
from app.debt_graphs import debt_metrics, formatted_debt_metrics
       
def create_table():
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
    debt_table.update_layout(title_text= symbol.upper())

    return debt_table

if __name__ == "__main__":
    try:
        symbol = get_symbol()
        balance_sheet_data = fetch_balance_data(symbol)
        income_sheet_data = fetch_income_data(symbol)

        num_years = len(balance_sheet_data['annualReports'])

        total_debt_metrics = calc_debt_metrics(symbol, num_years, balance_sheet_data, income_sheet_data, 
        debt_series, debt_ratios, coverage_ratios, reported_dates,
        form_debt_series, form_debt_ratios, form_coverage_ratios, debt_metrics)

        table = create_table()

        table.show()
    except:
        print("We couldn't find that symbol. Please try again with a valid symbol and API Key.")

