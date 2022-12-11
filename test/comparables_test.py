#This is the test file for the comparables program

from app.comparables import get_csv_url
from app.comparables import get_industry_companies
from app.comparables import get_comparable_companies
from app.comparables import get_comps_metrics
from app.comparables import create_comps_table
from app.comparables import comp_symbols, comp_values_diff, comp_industry, comp_marketcap, comparable_companies

#true_comp_symbols, true_comp_values, true_comps

#comp_total_debt = []
#comp_debt_ratio = []
#comp_coverage_ratio = []
#comp_debt_symbols = []
#comp_debt_metrics = {'Companies': comp_debt_symbols, 'TotalDebt': comp_total_debt,
#'DebtRatio': comp_debt_ratio, 'CoverageRatio': comp_coverage_ratio }


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
    industry_result = get_industry_companies(5574, industry_csv_data, 'Waste Management', comp_symbols, comp_values_diff, comp_industry, comp_marketcap, comparable_companies)
    assert isinstance(industry_result, dict)

    assert 'Symbols' in industry_result
    assert 'MarketCapDiff' in industry_result
    
    assert len(industry_result['Symbols']) > 4


def test_get_comparable_companies():
    comparable_result = get_comparable_companies()
    assert isinstance(comparable_result, dict)

    assert 'Symbols' in comparable_result

    assert len(comparable_result['Symbols']) <= 5



