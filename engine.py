import datetime

class Order:
    def __init__(self, order_id, side, price, qty):
        self.order_id = order_id
        self.side = side.upper()  # 'BUY' or 'SELL'
        self.price = float(price)
        self.qty = int(qty)
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return f"[{self.side}] ID: {self.order_id} | Price: {self.price} | Qty: {self.qty}"

class MarketMicrostructureEngine:
    def __init__(self):
        self.bid_book = []  # Buyers (Highest Price First)
        self.ask_book = []  # Sellers (Lowest Price First)
        self.trades = []    # History of executed matches

    def get_mid_price(self):
        """Calculates the fair market value between best bid and best ask."""
        if not self.bid_book or not self.ask_book:
            return None
        return (self.bid_book[0].price + self.ask_book[0].price) / 2.0

    def add_limit_order(self, order):
        """Standard entry point for limit orders with matching logic."""
        if order.side == 'BUY':
            self._match(order, self.ask_book)
        else:
            self._match(order, self.bid_book)

    def _match(self, order, opposite_book):
        """Core Matching Engine: Implements Price-Time Priority."""
        while order.qty > 0 and len(opposite_book) > 0:
            best_opposite = opposite_book[0]
            
            # Check if prices 'cross'
            if (order.side == 'BUY' and order.price >= best_opposite.price) or \
               (order.side == 'SELL' and order.price <= best_opposite.price):
                
                match_qty = min(order.qty, best_opposite.qty)
                print(f"MATCH: {match_qty} units @ {best_opposite.price}")
                
                # Execute Trade Logic
                order.qty -= match_qty
                best_opposite.qty -= match_qty
                self.trades.append({'price': best_opposite.price, 'qty': match_qty})

                if best_opposite.qty == 0:
                    opposite_book.pop(0)
            else:
                break
        
        # If order still has quantity, it becomes 'Passive' liquidity in the book
        if order.qty > 0:
            self._insert_into_book(order)

    def _insert_into_book(self, order):
        """Maintains sorted order books."""
        if order.side == 'BUY':
            self.bid_book.append(order)
            self.bid_book.sort(key=lambda x: x.price, reverse=True)
        else:
            self.ask_book.append(order)
            self.ask_book.sort(key=lambda x: x.price)

    def execute_market_order(self, side, qty):
        """Simulates an aggressive market participant and calculates Slippage."""
        arrival_price = self.get_mid_price()
        if arrival_price is None:
            print("Insufficient liquidity to determine Arrival Price.")
            return

        total_cost = 0
        total_qty_filled = 0
        target_book = self.ask_book if side == 'BUY' else self.bid_book

        print(f"\n--- EXECUTION LOG: {side} {qty} units ---")
        
        while qty > 0 and target_book:
            best_order = target_book[0]
            fill_qty = min(qty, best_order.qty)
            
            print(f"Filled {fill_qty} @ {best_order.price}")
            
            total_cost += fill_qty * best_order.price
            total_qty_filled += fill_qty
            qty -= fill_qty
            best_order.qty -= fill_qty
            
            if best_order.qty == 0:
                target_book.pop(0)

        # Transaction Cost Analysis (TCA)
        if total_qty_filled > 0:
            vwap = total_cost / total_qty_filled
            slippage = abs(vwap - arrival_price)
            print(f"RESULT: Filled {total_qty_filled} units")
            print(f"VWAP: {vwap:.4f} | Arrival Price: {arrival_price:.4f}")
            print(f"SLIPPAGE (Implementation Shortfall): {slippage:.4f}")
        else:
            print("Execution failed: No liquidity.")

# --- Demo Script ---
if __name__ == "__main__":
    engine = MarketMicrostructureEngine()

    # 1. SETUP: Create a "Ladder" of Sellers (Liquidity)
    print("--- Building the Order Book ---")
    engine.add_limit_order(Order(1, 'BUY', 99.0, 10))   # Best Bid (Sets the floor)
    engine.add_limit_order(Order(2, 'SELL', 100.0, 5))  # Cheapest Seller (5 units)
    engine.add_limit_order(Order(3, 'SELL', 101.0, 10)) # Expensive Seller (10 units)
    engine.add_limit_order(Order(4, 'SELL', 105.0, 10)) # Very Expensive Seller
    
    # 2. ACTION: Place a large MARKET BUY for 10 units
    engine.execute_market_order('BUY', 10)