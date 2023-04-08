import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load the data into a Pandas DataFrame
df = pd.read_csv('Stock_Data.csv')

# Create a new DataFrame with only the closing prices
prices = df[['Close']]

# Shift the prices so that the first row corresponds to today's price and the second row corresponds to yesterday's price
prices_shifted = prices.shift(1)

# Add a column with tomorrow's closing price
prices_shifted['Tomorrow'] = prices['Close']

# Drop the first row, which has a null value for yesterday's price
prices_shifted = prices_shifted.dropna()

# Separate the target variable (tomorrow's closing price) from the input features (yesterday's closing price)
X = prices_shifted[['Close']]
y = prices_shifted['Tomorrow']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Linear Regression model
model = LinearRegression()

# Train the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Calculate the test score
test_score = model.score(X_test, y_test)
print(f'Test score: {test_score:.2f}')

# Use the model to predict tomorrow's closing price based on today's closing price
today_close = df['Close'].iloc[-1]
tomorrow_close_prediction = model.predict([[today_close]])[0]
print(f'Predicted closing price for tomorrow: {tomorrow_close_prediction:.2f}')
