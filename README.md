# Stock Volatility Explorer 🚀

## Overview 📝
This project analyzes the volatility behavior of selected U.S. equities by computing rolling historical volatility and comparing stock-level risk relative to the overall market.
The goal is to understand how different stocks behave under normal and stress (high-volatility) market regimes.

## Motivation 📚
Volatility is a key measure of financial risk. While some stocks are inherently volatile, others become risky only during periods.

## Methodolgy 📖
- Retrieved historical daily price data for selected stocks and a market benchmark index (SPY) from yfinance,
- Computed daily returns from adjusted closing prices,
- Calculated rolling volatility using 20-day and 60-day windows,
- Measured relative volatility by normalizing stock volatility against market volatility,
- Identified high-volatility market regimes using percentile-based thresholds,
- Compared stock behavior during normal and stress market periods.

## Tools Used 🛠️
- Python
- pandas
- yfinance
- matplotlib
- Jupyter Notebook
