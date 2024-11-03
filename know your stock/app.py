from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from io import BytesIO
import base64

app = Flask(__name__)

def plot_stock_prices(ticker_symbol, start_date, end_date, graph_type):
    # Fetch historical stock data from Yahoo Finance
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

    # Extract the 'Close' prices
    closing_prices = stock_data['Close']

    # Plotting the closing prices
    plt.figure(figsize=(10, 6))
    if graph_type == 'line':
        plt.plot(closing_prices, color='blue', label='Closing Price')
    elif graph_type == 'bar':
        plt.bar(closing_prices.index,closing_prices, color='blue', label='Closing Price')
    else:
        return None

    # Save plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    ticker_symbol = request.form['ticker_symbol']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    graph_type = request.form['graph_type']

    plot_url = plot_stock_prices(ticker_symbol, start_date, end_date, graph_type)

    if plot_url:    
        return render_template('plot.html', plot_url=plot_url)
    else:
        return "Invalid input. Please try again."

if __name__ == '__main__':
    app.run(debug=True,port=8000)
