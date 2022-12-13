#This is the test file for the overview program

import requests
import json

from app.alpha import API_KEY
from app.overview import fetch_balance_data, fetch_income_data, calc_total_debt, format_debt, calc_debt_ratio, calc_coverage_ratio

def test_fetch_balance_data():
    balance_data = fetch_balance_data('AAPL')

    assert isinstance(balance_data, dict)

    assert 'annualReports' in balance_data

    assert len(balance_data['annualReports']) == 5.0

def test_fetch_income_data():
    income_data = fetch_income_data('IBM')

    assert isinstance(income_data, dict)

    assert 'annualReports' in income_data

    assert len(income_data['annualReports']) == 5.0

def test_calc_total_debt():
    balance_data = fetch_balance_data('GOOGL')

    total_debt = calc_total_debt('GOOGL', balance_data)

    assert isinstance(total_debt, float)

    assert total_debt >= 0.0

def test_format_debt():
    balance_data = fetch_balance_data('GOOGL')

    total_debt = calc_total_debt('GOOGL', balance_data)

    formatted_debt = format_debt('GOOGL', balance_data, total_debt)

    assert isinstance(formatted_debt, str)

    assert 'Billion' in formatted_debt


def test_calc_debt_ratio():
    balance_data = fetch_balance_data('BABA')
    total_debt = calc_total_debt('BABA', balance_data)

    debt_ratio = calc_debt_ratio('BABA', balance_data, total_debt)

    assert isinstance(debt_ratio, float)

    assert debt_ratio >= 0.0

def test_calc_coverage_ratio():
    income_data = fetch_income_data('META')

    coverage_ratio = calc_coverage_ratio('META', income_data)

    assert isinstance(coverage_ratio, float)

    

