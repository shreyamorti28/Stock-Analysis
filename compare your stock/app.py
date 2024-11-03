import matplotlib
matplotlib.use('Agg')  # Set the backend to non-GUI

from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from io import BytesIO
import base64

app = Flask(__name__)

def fetch_stock_data(ticker_symbol, start_date, end_date):
    """Fetch historical stock data from Yahoo Finance."""
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    return stock_data

def plot_graphs(stock_data1, stock_data2, ticker1, ticker2):
    """Plot the closing prices of two stocks."""
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data1['Close'], label=f'{ticker1} Closing Price', color='blue')
    plt.plot(stock_data2['Close'], label=f'{ticker2} Closing Price', color='orange')
    plt.title('Stock Comparison - Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    # Save to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)  # Move to the start of the BytesIO object

    # Encode the image to base64
    chart = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()  # Close the figure to free memory
    return f"data:image/png;base64,{chart}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            ticker_symbol1 = request.form['ticker_symbol1']
            ticker_symbol2 = request.form['ticker_symbol2']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            
            # Fetch historical stock data for both stocks
            stock_data1 = fetch_stock_data(ticker_symbol1, start_date, end_date)
            stock_data2 = fetch_stock_data(ticker_symbol2, start_date, end_date)

            # Plot graphs for both stocks
            chart = plot_graphs(stock_data1, stock_data2, ticker_symbol1, ticker_symbol2)

            return render_template('results.html', chart=chart)
        except KeyError as e:
            error_message = f'Missing key in form data: {e}'
            return render_template('index.html', error=error_message)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=4000)
