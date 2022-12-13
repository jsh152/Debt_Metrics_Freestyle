#This is the test file for the debt graphs program

from app.alpha import API_KEY
from app.overview import fetch_balance_data
from app.overview import fetch_income_data
from app.debt_graphs import debt_series, debt_ratios, coverage_ratios , reported_dates , form_debt_series , form_debt_ratios , form_coverage_ratios , debt_metrics, formatted_debt_metrics
from app.debt_graphs import calc_debt_metrics


def test_calc_debt_metrics():
    balance_sheet_data = fetch_balance_data('IBM')
    income_sheet_data = fetch_income_data('IBM')
    
    annual_debt_metrics = calc_debt_metrics('IBM', 5, balance_sheet_data, income_sheet_data, 
    debt_series, debt_ratios, coverage_ratios, reported_dates,
    form_debt_series, form_debt_ratios, form_coverage_ratios, debt_metrics)

    assert isinstance(annual_debt_metrics, dict)

    assert 'totaldebt' in annual_debt_metrics
    assert 'coverageratio' in annual_debt_metrics

    assert len(annual_debt_metrics['totaldebt']) == 5.0