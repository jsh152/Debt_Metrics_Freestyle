# Debt_Metrics_Freestyle
This is a program that allows the user to input a publicly listed company and have relevant debt metrics displayed about it.

The debt metrics currently calculated and displayed are: Total Debt, Debt/Asset Ratio, and Interest Coverage Ratio.

This program also displays how these metrics have changed over the past 5 years and what the metrics currently are for comparable companies.

## Setup

Create and activate a virtual environment:

```sh
conda create -n freestyle-env python=3.8

conda activate freestyle-env
```

Install package dependencies:
```sh
pip install -r requirements.txt
```

## Configuration


[Obtain an API Key](https://www.alphavantage.co/support/#api-key) from AlphaVantage.

Then create a local .env file and provide the key like this:
```sh
# this is the ".env" file...
API_KEY="{Insert API Key here}"
```

## Usage
There are 4 different programs that the user can run from the command line:
    1. 'overview': Displays the current debt metrics for a chosen company
    2. 'debt_graphs': Displays graphs depicting how debt metrics for chosen company have changed over the past 5 years
    3. 'debt_table': Displays a table depicting how debt metrics for chosen company have changed over the past 5 yeras
    4. 'comparables': Displays a table depicting current debt metrics for chosen company and 3 comparable companies


Run the overview program:
```sh
python -m app.overview
```

Run debt graphs program:
```sh
python -m app.debt_graphs
```

Run debt table program:
```sh
python -m app.debt_table
```

Run comparables program:
```sh
python -m app.comparables
```

## Testing

Run tests:

```sh
pytest
```

