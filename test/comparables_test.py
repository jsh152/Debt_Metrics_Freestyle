#This is the test file for the comparables program

from app.comparables import get_csv_url
from app.comparables import get_industry_companies
from app.comparables import get_comparable_companies
from app.comparables import get_comps_metrics
from app.comparables import create_comps_table
from app.comparables import comp_symbols, comp_values_diff, comp_industry, comp_marketcap, comparable_companies

from pandas import DataFrame

def test_get_csv_url():
    csv_result =  get_csv_url()
    assert isinstance(csv_result, DataFrame)

    assert 'Symbol' in csv_result.columns
    assert 'Industry' in csv_result.columns
    assert 'Market Cap' in csv_result.columns

    assert len(csv_result) > 1000
    


def test_get_industry_companies():
    industry_csv_data = get_csv_url()
    industry_result = get_industry_companies(5574, 5560, industry_csv_data, 'Waste Management', comp_symbols, comp_values_diff, comp_industry, comp_marketcap, comparable_companies)
    assert isinstance(industry_result, dict)

    assert 'Symbols' in industry_result
    assert 'MarketCapDiff' in industry_result
    
    assert len(industry_result['Symbols']) > 4





