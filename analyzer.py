import requests
import pandas as pd

def analyze_stock(ticker):
    #NSE stock check
    if not ticker.endswith(".NS"):
        ticker = f"{ticker}.NS"
    
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=6mo"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        data = response.json()

        #Price and Volume
        prices = data['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
        volumes = data['chart']['result'][0]['indicators']['quote'][0]['volume']
        
        df = pd.DataFrame({'Close': prices, 'Volume': volumes}).dropna()

        #RSI logic
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]

        #Volume Check
        avg_vol = df['Volume'].rolling(window=20).mean().iloc[-1]
        vol_ratio = df['Volume'].iloc[-1] / avg_vol

        #Return results
        return {
            "Ticker": ticker,
            "Price": round(df['Close'].iloc[-1], 2),
            "RSI": round(rsi, 2),
            "Signal": "BULLISH" if rsi < 30 else "BEARISH" if rsi > 70 else "NEUTRAL"
        }
    except:
        return None

#Main Program Loop 
print("___Aayush's Simple Stock Analyzer___")
watchlist = []

while True:
    user_input = input("\nEnter Stock Name, then type 'DONE' to see results: ").strip().upper()
    
    if user_input == 'DONE':
        break
    
    result = analyze_stock(user_input)
    if result:
        watchlist.append(result)
        print(f"Added {user_input} to watchlist.")
    else:
        print("Invalid Stock. Please try again.")

#Final results 
if watchlist:
    print("\n" + "="*40)
    print(f"{'TICKER':<12} {'PRICE':<10} {'RSI':<8} {'SIGNAL'}")
    print("-" * 40)
    for s in watchlist:
        print(f"{s['Ticker']:<12} ₹{s['Price']:<9} {s['RSI']:<8} {s['Signal']}")
    print("="*40)