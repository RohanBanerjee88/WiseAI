import tkinter
import yfinance as yf
import csv
import pandas as pd
import matplotlib.pyplot as plt
import openai
import tkinter as tk


def read_stock_data():
    stock_dict = {}
    with open('Stock_Data.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader)
        for row in reader:
            # Add a check to ensure that the row has at least 2 columns
            if len(row) >= 2:
                stock_dict[row[1]] = row[0]
    return stock_dict


stock_dict = read_stock_data()


def get_stock_price(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    open_price = stock_data['Open'].iloc[0]
    close_price = stock_data['Close'].iloc[-1]
    return open_price, close_price


def display_stock_history(symbol):
    # Get the stock data from Yahoo Finance
    stock = yf.Ticker(symbol)

    # Get the historical data of the stock
    historical_data = stock.history(period="max")

    # Get the daily returns of the stock
    daily_returns = historical_data['Close'].pct_change()

    # Display the historical data
    return historical_data, daily_returns


def show_institutional_holders(symbol):
    # Get the stock data from Yahoo Finance
    stock = yf.Ticker(symbol)

    # Get the institutional holders of the stock
    institutional_holders = stock.institutional_holders

    return institutional_holders
    # Display the institutional holders



def show_mutual_holders(symbol):
    # Get the stock data from Yahoo Finance
    stock = yf.Ticker(symbol)

    # Get the institutional holders of the stock
    mutual_holders = stock.mutualfund_holders

    return mutual_holders


def show_stock_graph(symbol):
    # Get the stock data from Yahoo Finance
    stock = yf.Ticker(symbol)

    # Get the historical data of the stock
    historical_data = stock.history(period="max")

    # Create the stock graph
    plt.plot(historical_data.index, historical_data['Close'])
    plt.title(symbol + " Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")

    # Display the stock graph
    return plt.show()


# Set up the OpenAI API credentials
openai.api_key = "Your OPEN AI API KEY"


def recommend_buy_or_sell(symbol):
    # Get the stock data from Yahoo Finance
    stock = yf.Ticker(symbol)

    # Get the historical data of the stock and the daily returns
    historical_data, daily_returns = display_stock_history(symbol)

    # Use OpenAI GPT to analyze the daily returns and recommend buy or sell
    prompt = "Based on the daily returns of " + symbol + ", should I buy or sell this stock?"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=250,
        n=1,
        stop=None,
        timeout=15,
        presence_penalty=0.5,
        frequency_penalty=0.5,
        best_of=3
    )

    # Get the recommended action from the OpenAI response
    recommended_action = response.choices[0].text.strip()

    # Return the recommended action
    return recommended_action



########################################################################################################################
#########################################  GUI #########################################################################

class StockAnalyzerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.stock_dict = read_stock_data()
        self.create_widgets()

    def show_graph(self):
        symbol = self.symbol_entry.get()
        if symbol in self.stock_dict:
            show_stock_graph(self.stock_dict[symbol])
        elif symbol:
            show_stock_graph(symbol)
        else:
            self.recommendation_label.configure(text="Symbol not found, please try again.")

    def get_recommendation(self):
        symbol = self.symbol_entry.get()
        if symbol in self.stock_dict:
            recommendation = recommend_buy_or_sell(self.stock_dict[symbol])
            self.recommendation_label.configure(text="Recommendation: " + recommendation)
        elif symbol:
            recommendation = recommend_buy_or_sell(symbol)
            self.recommendation_label.configure(text="Recommendation: " + recommendation)
        else:
            self.recommendation_label.configure(text="Symbol not found, please try again.")

    def display_history(self):
        symbol = self.symbol_entry.get()
        if symbol in self.stock_dict:
            historical_data, daily_returns = display_stock_history(stock_dict[symbol])
            # create a new window to display the historical data
            history_window = tk.Toplevel(self.master)
            history_window.title(symbol + " Historical Data")

            # create a text widget to display the historical data
            history_text = tk.Text(history_window)
            history_text.insert(tk.END, "Historical Data:\n")
            history_text.insert(tk.END, historical_data.to_string())
            history_text.insert(tk.END, "\n\nDaily Returns:\n")
            history_text.insert(tk.END, daily_returns.to_string())
            history_text.pack()
        elif symbol:
            historical_data, daily_returns = display_stock_history(symbol)
            # create a new window to display the historical data
            history_window = tk.Toplevel(self.master)
            history_window.title(symbol + " Historical Data")

            # create a text widget to display the historical data
            history_text = tk.Text(history_window)
            history_text.insert(tk.END, "Historical Data:\n")
            history_text.insert(tk.END, historical_data.to_string())
            history_text.insert(tk.END, "\n\nDaily Returns:\n")
            history_text.insert(tk.END, daily_returns.to_string())
            history_text.pack()

        else:
            self.recommendation_label.configure(text="Please enter a symbol.")

    def show_institutional(self):
        symbol = self.symbol_entry.get()
        if symbol in self.stock_dict:
            institutional_holders = show_institutional_holders(stock_dict[symbol])
            # create a new window to display the institutional holders
            institutional_window = tk.Toplevel(self.master)
            institutional_window.title(symbol + " Institutional Holders")

            # create a text widget to display the institutional holders
            institutional_text = tk.Text(institutional_window)
            institutional_text.insert(tk.END, "Institutional Holders:\n")
            institutional_text.insert(tk.END, institutional_holders.to_string())
            institutional_text.pack()
        elif symbol:
            institutional_holders = show_institutional_holders(symbol)
            # create a new window to display the institutional holders
            institutional_window = tk.Toplevel(self.master)
            institutional_window.title(symbol + " Institutional Holders")

            # create a text widget to display the institutional holders
            institutional_text = tk.Text(institutional_window)
            institutional_text.insert(tk.END, "Institutional Holders:\n")
            institutional_text.insert(tk.END, institutional_holders.to_string())
            institutional_text.pack()

        else:
            self.recommendation_label.configure(text="Please enter a symbol.")

    def show_mutual(self):
        symbol = self.symbol_entry.get()
        if symbol in self.stock_dict:
            mutual_holders = show_mutual_holders(stock_dict[symbol])
            # create a new window to display the mutual fund holders
            mutual_window = tk.Toplevel(self.master)
            mutual_window.title(symbol + " Mutual Fund Holders")

            # create a text widget to display the mutual fund holders
            mutual_text = tk.Text(mutual_window)
            mutual_text.insert(tk.END, "Mutual Fund Holders:\n")
            mutual_text.insert(tk.END, mutual_holders.to_string())
            mutual_text.pack()
        elif symbol:
            mutual_holders = show_mutual_holders(symbol)
            # create a new window to display the mutual fund holders
            mutual_window = tk.Toplevel(self.master)
            mutual_window.title(symbol + " Mutual Fund Holders")

            # create a text widget to display the mutual fund holders
            mutual_text = tk.Text(mutual_window)
            mutual_text.insert(tk.END, "Mutual Fund Holders:\n")
            mutual_text.insert(tk.END, mutual_holders.to_string())
            mutual_text.pack()
        else:
            self.recommendation_label.configure(text="Please enter a symbol.")

    def create_widgets(self):
        self.symbol_label = tk.Label(self.master, text="Enter stock symbol or Name:")
        self.symbol_entry = tk.Entry(self.master, width=10)
        self.graph_button = tk.Button(self.master, text="Show Graph", command=self.show_graph)
        self.recommendation_button = tk.Button(self.master, text="Get Recommendation", command=self.get_recommendation)
        self.history_button = tk.Button(self.master, text="Show Historical Data", command=self.display_history)
        self.institutional_holders_button = tk.Button(self.master, text="Show Institutional Holders", command=self.show_institutional)
        self.mutual_holders_button = tk.Button(self.master, text="Show Mutual Fund Holders", command=self.show_mutual)
        self.recommendation_label = tk.Label(self.master, text="")
        self.symbol_label.grid(row=0, column=0)
        self.symbol_entry.grid(row=0, column=1)
        self.graph_button.grid(row=1, column=0)
        self.recommendation_button.grid(row=1, column=1)
        self.history_button.grid(row=1, column=2)
        self.institutional_holders_button.grid(row=2, column=0)
        self.mutual_holders_button.grid(row=2, column=1)
        self.recommendation_label.grid(row=3, column=0, columnspan=3)

root = tk.Tk()
app = StockAnalyzerGUI(master=root)
app.mainloop()

########################################################################################################################

