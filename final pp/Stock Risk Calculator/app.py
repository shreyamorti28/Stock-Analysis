from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import yfinance as yf

app = Flask(__name__)

# Define functions to process data
def fetch_stock_data(ticker_symbol, start_date, end_date):
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    return data['Close']

def calculate_volatility(returns):
    return returns.std() * np.sqrt(252)

def calculate_var(returns, alpha=0.05):
    return np.percentile(returns, alpha * 100)

def calculate_cvar(returns, alpha=0.05):
    var = calculate_var(returns, alpha)
    return returns[returns <= var].mean()

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    ticker_symbol = request.form['ticker_symbol']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    # Fetch historical stock data
    stock_data = fetch_stock_data(ticker_symbol, start_date, end_date)

    # Calculate daily returns
    returns = stock_data.pct_change().dropna()

    # Calculate risk metrics
    volatility = calculate_volatility(returns)
    var_5 = calculate_var(returns)
    cvar_5 = calculate_cvar(returns)

    # Render results template with risk metrics
    return render_template('results.html', 
                           volatility=volatility,
                           var_5=var_5,
                           cvar_5=cvar_5)

if __name__ == '__main__':
    app.run(debug=True,port=2000)
