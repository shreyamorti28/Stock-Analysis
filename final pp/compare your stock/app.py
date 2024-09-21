from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

app = Flask(__name__)

# Define functions
def fetch_ticker_symbols(company_names):
    ticker_symbols = []
    for company in company_names:
        try:
            ticker = yf.Ticker(company)
            symbol = ticker.info['symbol']
            ticker_symbols.append(symbol)
        except KeyError:
            print(f"Error: Ticker symbol not found for {company}. Skipping...")
    return ticker_symbols

def fetch_stock_data(ticker_symbols, start_date, end_date):
    stock_data = {}
    for symbol in ticker_symbols:
        data = yf.download(symbol, start=start_date, end=end_date)
        stock_data[symbol] = data['Close']
    return stock_data

def plot_stock_comparison(stock_data, chart_type):
    plt.figure(figsize=(10, 6))
    for symbol, data in stock_data.items():
        if chart_type == 'closing prices':
            plt.plot(data, label=symbol)
            plt.ylabel('Price (USD)')
        elif chart_type == 'returns':
            returns = data.pct_change() * 100
            plt.plot(returns, label=symbol)
            plt.ylabel('Percentage Returns')
        else:
            print("Invalid chart type. Please choose 'closing prices' or 'returns'.")
            return

    plt.title('Historical Stock Comparison')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)

    # Save plot as a file
    plt.savefig('static/chart.png')

# Define routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_names = request.form['company_names'].split(',')
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        chart_type = request.form['chart_type'].lower()

        ticker_symbols = fetch_ticker_symbols(company_names)

        if ticker_symbols:
            stock_data = fetch_stock_data(ticker_symbols, start_date, end_date)
            plot_stock_comparison(stock_data, chart_type)

            return render_template('results.html', chart='static/chart.png')
        else:
            return render_template('index.html', error="No valid ticker symbols found. Please check your input company names.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=4000)