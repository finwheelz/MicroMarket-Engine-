import random
import pandas as pd
import numpy as np
from engine import MarketMicrostructureEngine, Order

# --- CONFIGURATION ---
NUM_STEPS = 5000       # How many "ticks" of time to simulate
START_PRICE = 100.0    # The starting stock price
VOLATILITY = 0.2       # How much the price wiggles (Standard Deviation)

def run_simulation():
    engine = MarketMicrostructureEngine()
    
    # Fundamental "True Value" of the stock (Random Walk)
    true_price = START_PRICE
    
    # Data Storage
    data_log = []

    print(f"--- STARTING SIMULATION: {NUM_STEPS} Steps ---")

    for t in range(NUM_STEPS):
        # 1. Update the "True Value" (Random Walk)
        # The price drifts up or down randomly
        true_price += np.random.normal(0, VOLATILITY)
        
        # 2. MARKET MAKERS (Provide Liquidity)
        # They place Limit Orders around the True Price
        bid_price = round(true_price - random.uniform(0.1, 0.5), 2)
        ask_price = round(true_price + random.uniform(0.1, 0.5), 2)
        
        # Add liquidity to book
        engine.add_limit_order(Order(t, 'BUY', bid_price, random.randint(1, 10)))
        engine.add_limit_order(Order(t, 'SELL', ask_price, random.randint(1, 10)))

        # 3. NOISE TRADERS (Take Liquidity)
        # Randomly decide to Buy or Sell aggressively
        if random.random() < 0.3:  # 30% chance of a trade happening
            side = 'BUY' if random.random() > 0.5 else 'SELL'
            qty = random.randint(1, 5)
            engine.execute_market_order(side, qty)

        # 4. CAPTURE DATA (The "Snapshot")
        # This is what the AI will study later
        mid_price = engine.get_mid_price()
        best_bid = engine.bid_book[0].price if engine.bid_book else np.nan
        best_ask = engine.ask_book[0].price if engine.ask_book else np.nan
        spread = best_ask - best_bid if (best_ask and best_bid) else np.nan
        
        # Calculate Order Imbalance (Are there more Buyers or Sellers?)
        bid_vol = sum([o.qty for o in engine.bid_book[:5]]) # Top 5 levels
        ask_vol = sum([o.qty for o in engine.ask_book[:5]])
        imbalance = (bid_vol - ask_vol) / (bid_vol + ask_vol + 1e-9)

        if mid_price:
            data_log.append({
                'Time': t,
                'MidPrice': mid_price,
                'BestBid': best_bid,
                'BestAsk': best_ask,
                'Spread': spread,
                'Imbalance': imbalance,
                'TruePrice': true_price  # We know this, but the AI has to guess it!
            })

    # 5. EXPORT TO CSV
    df = pd.DataFrame(data_log)
    df.to_csv('market_data.csv', index=False)
    print(f"--- SIMULATION COMPLETE. Saved {len(df)} rows to 'market_data.csv' ---")
    print(df.head())

if __name__ == "__main__":
    run_simulation()