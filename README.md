# Debt_Metrics_Freestyle


## Setup

Create and activate a virtual environment

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

