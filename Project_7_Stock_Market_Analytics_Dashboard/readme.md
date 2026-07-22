# 📈 Stock Market Analytics using Python

## Overview

This project is a Python-based Stock Market Analytics application that downloads one year of historical stock market data using the Yahoo Finance API (`yfinance`), performs data transformation and analysis using `pandas`, and visualizes the results using `matplotlib`.

The project demonstrates an end-to-end data analysis workflow:

Data Collection → Data Transformation → Data Analysis → Data Visualization

---

## Features

### Data Collection
- Download one year of historical stock data from Yahoo Finance
- Supports analysis of multiple stocks simultaneously
- Basic error handling for invalid stock symbols

### Data Transformation
Calculates the following metrics for each stock:

- Previous Closing Price
- Daily Price Change
- Daily Return (%)
- 7-Day Simple Moving Average (SMA)
- 20-Day Simple Moving Average (SMA)
- 30-Day Simple Moving Average (SMA)
- 20-Day Rolling Volatility
- Normalized Closing Price (Base = 100)

---

## Data Analysis

For every stock, the program calculates:

- Positive Trading Days
- Negative Trading Days
- Highest Daily Return
- Highest Volatility
- Lowest Volatility
- Average Volatility
- Monthly Average Closing Price
- Monthly Highest Closing Price
- Monthly Average Trading Volume
- Weekly Average Closing Price

---

## Watchlist Analysis

The application compares all selected stocks and calculates:

- Average Daily Return
- Average Volatility
- Highest Closing Price
- Lowest Closing Price
- Current Closing Price
- Total Return
- Highest Trading Volume
- Average Trading Volume
- Positive Trading Days
- Negative Trading Days

It also identifies:

- Best Performing Stock
- Worst Performing Stock
- Most Volatile Stock
- Least Volatile Stock
- Correlation Matrix
- Most Correlated Stock Pair
- Least Correlated Stock Pair

---

## Visualizations

The project includes the following visualizations:

1. Stock Price Comparison
2. Normalized Stock Performance Comparison
3. Closing Price vs SMA (20-Day)
4. Total Return Bar Chart
5. Daily Return Distribution (Histogram)
6. Daily Return vs Trading Volume (Scatter Plot)
7. Correlation Heatmap

---

## Libraries Used

- pandas
- yfinance
- matplotlib

Install the required libraries using:

```bash
pip install pandas matplotlib yfinance
```

---

## Project Structure

```
Stock-Market-Analytics/
│
├── stock_analysis.py
├── README.md
```

---

## Workflow

```
Download Stock Data
        │
        ▼
Transform Data
        │
        ▼
Analyze Individual Stocks
        │
        ▼
Analyze Complete Watchlist
        │
        ▼
Generate Visualizations
```

---

## How to Run

Clone the repository and run:

```bash
python stock_analysis.py
```

Modify the `scrip_list` inside the `main()` function to analyze different stocks.

Example:

```python
scrip_list = [
    "TCS.NS",
    "INFY.NS",
    "RELIANCE.NS"
]
```

---

## Skills Demonstrated

- Python Programming
- Data Collection using APIs
- Data Cleaning and Transformation
- Exploratory Data Analysis (EDA)
- Financial Data Analysis
- Data Visualization
- Time Series Analysis
- Code Modularization
- Basic Error Handling

---

## Future Improvements

Possible enhancements include:

- Interactive dashboard using Plotly/Dash
- Export analysis results to CSV or Excel
- Support for custom date ranges
- Additional technical indicators (EMA, RSI, MACD)
- Portfolio analysis
- Risk vs Return comparison

---

## Author : Rudra Chauhan

Developed as a Python Data Analysis project for learning ETL, financial data analysis, and visualization.