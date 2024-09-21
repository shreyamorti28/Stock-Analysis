from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from io import BytesIO
import base64

app = Flask(__name__)

def fetch_stock_data(ticker_symbol, start_date, end_date):
    """
    Fetch historical stock data for a ticker symbol.
    """
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    return data

def plot_closing_prices(data):
    """
    Plot closing prices over time.
    """
    fig = plt.figure(figsize=(8, 6))
    plt.plot(data['Close'], label='Closing Prices')
    plt.title('Closing Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    return fig

def plot_daily_returns(data):
    """
    Plot daily returns over time.
    """
    returns = data['Close'].pct_change() * 100
    fig = plt.figure(figsize=(8, 6))
    plt.plot(returns, label='Daily Returns')
    plt.title('Daily Returns Over Time')
    plt.xlabel('Date')
    plt.ylabel('Returns (%)')
    plt.legend()
    return fig

def plot_volume(data):
    """
    Plot trading volume over time.
    """
    fig = plt.figure(figsize=(8, 6))
    plt.plot(data['Volume'], label='Volume')
    plt.title('Trading Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.legend()
    return fig

def plot_histogram(data):
    """
    Plot histogram of closing prices.
    """
    fig = plt.figure(figsize=(8, 6))
    plt.hist(data['Close'], bins=20, edgecolor='black')
    plt.title('Histogram of Closing Prices')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    return fig

def plot_graphs(stock_data):
    """
    Plot all graphs and return their base64 encoded strings.
    """
    figs = []

    fig = plot_closing_prices(stock_data)
    figs.append(fig)

    fig = plot_daily_returns(stock_data)
    figs.append(fig)

    fig = plot_volume(stock_data)
    figs.append(fig)

    fig = plot_histogram(stock_data)
    figs.append(fig)

    plot_urls = []

    for fig in figs:
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close(fig)
        plot_urls.append(plot_url)

    return plot_urls

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker_symbol = request.form['ticker_symbol']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Fetch historical stock data
        stock_data = fetch_stock_data(ticker_symbol, start_date, end_date)

        # Plot all graphs
        plot_urls = plot_graphs(stock_data)

        return render_template('results.html', plot_urls=plot_urls)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
