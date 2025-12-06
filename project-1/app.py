
# app.py

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from backend import (
    get_price_data,
    calculate_portfolio_value,
    calculate_daily_returns,
    calculate_volatility,
    calculate_sharpe_ratio,
    calculate_var,
    calculate_drawdowns,
    calculate_correlation,
    get_asset_allocation
)

st.set_page_config(page_title="Portfolio Risk Dashboard", layout="wide")
st.title("📊 Portfolio Risk Dashboard")

# -------------------
# Sidebar Inputs
# -------------------
st.sidebar.header("Portfolio Inputs")

tickers_input = st.sidebar.text_input("Enter tickers separated by commas", "AAPL,MSFT,TSLA,GOOGL")
tickers = [t.strip().upper() for t in tickers_input.split(",")]

weights_input = st.sidebar.text_input("Enter weights separated by commas", "0.25,0.25,0.25,0.25")
try:
    weights = np.array([float(w.strip()) for w in weights_input.split(",")])
    if not np.isclose(weights.sum(), 1.0):
        st.sidebar.warning("Weights do not sum to 1. They will be normalized.")
        weights = weights / weights.sum()
except:
    st.sidebar.error("Invalid weights. Using equal weights.")
    weights = np.ones(len(tickers)) / len(tickers)

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-12-06"))
initial_investment = st.sidebar.number_input("Initial Investment ($)", min_value=1000.0, value=10000.0, step=1000.0)

# -------------------
# Fetch price data
# -------------------
st.write("Fetching price data from Yahoo Finance...")
price_data = get_price_data(tickers, start_date, end_date)

if price_data.empty:
    st.error("No price data returned for your tickers. Check tickers or date range.")
    st.stop()

# -------------------
# Portfolio calculations
# -------------------
portfolio_value = calculate_portfolio_value(price_data, weights, initial_investment)
daily_returns = calculate_daily_returns(portfolio_value)
volatility = calculate_volatility(daily_returns)
sharpe_ratio = calculate_sharpe_ratio(daily_returns)
var_5 = calculate_var(daily_returns)
drawdowns = calculate_drawdowns(portfolio_value)
correlation = calculate_correlation(price_data)
allocation = get_asset_allocation(weights, tickers)

# -------------------
# Display KPIs
# -------------------
st.subheader("📌 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Portfolio Value ($)", f"{portfolio_value[-1]:,.2f}")
col2.metric("Volatility (%)", f"{volatility*100:.2f}")
col3.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
col4.metric("VaR 5% (%)", f"{var_5*100:.2f}")
col5.metric("Max Drawdown (%)", f"{drawdowns.min()*100:.2f}")

# -------------------
# Charts
# -------------------
st.subheader("📈 Portfolio Growth")
st.line_chart(portfolio_value)

st.subheader("📉 Drawdowns")
st.line_chart(drawdowns)

st.subheader("📊 Daily Returns Distribution")
fig_hist = px.histogram(daily_returns, nbins=50, title="Daily Returns Histogram")
st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("🥧 Asset Allocation")
fig_pie = px.pie(names=allocation.index, values=allocation.values, title="Portfolio Allocation")
st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("🔗 Correlation Matrix")
fig_corr = px.imshow(correlation, text_auto=True, color_continuous_scale="RdBu_r", origin='lower')
st.plotly_chart(fig_corr, use_container_width=True)

import plotly
import streamlit as st
st.write("Plotly version:", plotly.__version__)
