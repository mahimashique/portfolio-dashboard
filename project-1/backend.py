# backend.py

import yfinance as yf
import pandas as pd
import numpy as np

# -------------------
# 1️⃣ Fetch price data
# -------------------
def get_price_data(tickers, start_date, end_date):
    """
    Fetch adjusted close prices from Yahoo Finance.
    Handles new yfinance behavior where 'Adj Close' may not exist.
    """
    try:
        data = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=False  # keeps Adj Close column
        )
        # Fallback if Adj Close missing
        if 'Adj Close' in data:
            data = data['Adj Close']
        else:
            print("Adj Close column not found. Using Close prices instead.")
            data = data['Close']

        if data.empty:
            print("No price data returned. Check tickers or date range.")
        return data

    except Exception as e:
        print("Error fetching data:", e)
        return pd.DataFrame()


# -------------------
# 2️⃣ Portfolio calculations
# -------------------
def calculate_portfolio_value(price_data, weights, initial_investment):
    if price_data.empty:
        return pd.Series(dtype=float)
    normalized = price_data / price_data.iloc[0]
    weighted = normalized * weights
    portfolio_value = weighted.sum(axis=1) * initial_investment
    return portfolio_value

def calculate_daily_returns(portfolio_value):
    return portfolio_value.pct_change().dropna()

def calculate_volatility(daily_returns):
    return daily_returns.std() * np.sqrt(252)

def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.0):
    vol = calculate_volatility(daily_returns)
    if vol == 0:
        return np.nan
    annual_return = daily_returns.mean() * 252
    return (annual_return - risk_free_rate) / vol

def calculate_var(daily_returns, confidence_level=0.05):
    if daily_returns.empty:
        return np.nan
    return np.percentile(daily_returns, confidence_level*100)

def calculate_drawdowns(portfolio_value):
    if portfolio_value.empty:
        return pd.Series(dtype=float)
    running_max = portfolio_value.cummax()
    drawdowns = (portfolio_value - running_max) / running_max
    return drawdowns

def calculate_correlation(price_data):
    if price_data.empty:
        return pd.DataFrame()
    return price_data.pct_change().corr()

def get_asset_allocation(weights, tickers):
    return pd.Series(weights, index=tickers)


