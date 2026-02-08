import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from engine import MarketMicrostructureEngine, Order

class RiskManager:
    def __init__(self, data_file='market_data.csv'):
        # Load the simulation data
        self.df = pd.read_csv(data_file)
        # Calculate Percentage Returns for Risk Metrics
        self.df['Returns'] = self.df['MidPrice'].pct_change()
        self.df = self.df.dropna()

    def calculate_market_risk(self, confidence_level=0.95):
        """Calculates VaR and Expected Shortfall (ES)."""
        percentile = (1 - confidence_level) * 100
        var = np.percentile(self.df['Returns'], percentile)
        
        # Expected Shortfall (Average loss beyond VaR)
        tail_losses = self.df[self.df['Returns'] <= var]['Returns']
        es = tail_losses.mean()
        
        return var, es

    def run_liquidity_stress_test(self, sell_volume=50):
        """
        Simulates a 'Black Swan' where 80% of buyers disappear.
        Measures the execution cost in a 'dry' market.
        """
        stress_engine = MarketMicrostructureEngine()
        
        # 1. SETUP: Create a healthy Two-Sided Market
        # We need both BUYERS and SELLERS to have a Mid-Price
        for i in range(1, 21):
            # Buyers @ 99.9, 99.8, ...
            stress_engine.add_limit_order(Order(i, 'BUY', 100 - (i*0.1), 10))
            # Sellers @ 100.1, 100.2, ...
            stress_engine.add_limit_order(Order(i+100, 'SELL', 100 + (i*0.1), 10))
        
        initial_mid = stress_engine.get_mid_price()
        
        # 2. THE BLACK SWAN: Remove 80% of the Buyers
        # We simulate a "Liquidity Pull" where buyers cancel their orders in panic
        # Only the top 4 buy orders remain
        stress_engine.bid_book = stress_engine.bid_book[:4] 
        
        print(f"\n--- STRESS TEST: {sell_volume} UNIT LIQUIDATION ---")
        print(f"Pre-Crash Mid Price: {initial_mid}")
        
        # 3. EXECUTE EMERGENCY SALE
        # We sell into the thinned-out book to see the crash
        stress_engine.execute_market_order('SELL', sell_volume)
        
    def plot_risk_distribution(self, var, es):
        """Visualizes the 'Fat Tails' of the market."""
        plt.figure(figsize=(10, 6))
        # Plot histogram of returns
        plt.hist(self.df['Returns'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        # Add Vertical Lines for Risk Metrics
        plt.axvline(var, color='red', linestyle='--', linewidth=2, label=f'VaR (95%): {var:.4%}')
        plt.axvline(es, color='darkred', linestyle='-', linewidth=2, label=f'Exp Shortfall: {es:.4%}')
        
        plt.title("Market Risk Distribution (Daily Returns)")
        plt.xlabel("Returns")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.show()

# --- Execution ---
if __name__ == "__main__":
    rm = RiskManager()
    
    # 1. Statistical Risk (VaR & ES)
    var_95, es_95 = rm.calculate_market_risk(0.95)
    
    print("--- STATISTICAL RISK METRICS ---")
    print(f"95% Value-at-Risk (VaR): {var_95:.4%}")
    print(f"95% Expected Shortfall (ES): {es_95:.4%}")
    print(f"Interpretation: In a crash, you lose an average of {abs(es_95):.2%} per tick.")

    # 2. Liquidity Stress Test (The Black Swan)
    rm.run_liquidity_stress_test(sell_volume=60)

    # 3. Visualization
    rm.plot_risk_distribution(var_95, es_95)