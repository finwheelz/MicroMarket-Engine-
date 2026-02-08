import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from engine import MarketMicrostructureEngine, Order
from risk_management import RiskManager
import time


st.set_page_config(page_title="Liquid-Risk Terminal", layout="wide")
st.title("Liquid-Risk: Institutional Trading Dashboard")



if 'engine' not in st.session_state:
    st.session_state.engine = MarketMicrostructureEngine()
    # Initialize with some liquidity
    for i in range(1, 6):
        st.session_state.engine.add_limit_order(Order(i, 'BUY', 100 - i*0.5, 10))
        st.session_state.engine.add_limit_order(Order(i+10, 'SELL', 100 + i*0.5, 10))

# --- SIDEBAR: TRADING PANEL ---
st.sidebar.header("Execution Panel")
order_type = st.sidebar.radio("Order Type", ["Market Order", "Limit Order"])
side = st.sidebar.selectbox("Side", ["BUY", "SELL"])
qty = st.sidebar.number_input("Quantity", min_value=1, value=10)

if order_type == "Limit Order":
    price = st.sidebar.number_input("Price", min_value=1.0, value=100.0)
    if st.sidebar.button("Place Limit Order"):
        order = Order(int(time.time()), side, price, qty)
        st.session_state.engine.add_limit_order(order)
        st.sidebar.success(f"Limit {side} placed at {price}")

else: # Market Order
    if st.sidebar.button("Execute Market Order"):
        st.session_state.engine.execute_market_order(side, qty)
        st.sidebar.warning(f"Market {side} executed for {qty} units")

# --- MAIN DASHBOARD ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Market Depth (Level 2 Data)")
    
    # 1. Prepare Data for Visualization
    bids = sorted(st.session_state.engine.bid_book, key=lambda x: x.price, reverse=True)
    asks = sorted(st.session_state.engine.ask_book, key=lambda x: x.price)
    
    bid_df = pd.DataFrame([{'Price': o.price, 'Qty': o.qty, 'Side': 'Bid'} for o in bids])
    ask_df = pd.DataFrame([{'Price': o.price, 'Qty': o.qty, 'Side': 'Ask'} for o in asks])
    
    if not bid_df.empty and not ask_df.empty:
        # 2. Create the Depth Chart
        fig = go.Figure()
        fig.add_trace(go.Bar(x=bid_df['Price'], y=bid_df['Qty'], name='Bids', marker_color='green'))
        fig.add_trace(go.Bar(x=ask_df['Price'], y=ask_df['Qty'], name='Asks', marker_color='red'))
        fig.update_layout(title="Limit Order Book Depth", xaxis_title="Price", yaxis_title="Volume")
        st.plotly_chart(fig, use_container_width=True)
        
        # 3. Show Mid Price
        mid_price = st.session_state.engine.get_mid_price()
        st.metric(label="Current Mid-Price", value=f"${mid_price:.2f}")
    else:
        st.warning("Order Book is Empty! Add orders via sidebar.")

with col2:
    st.subheader("Risk Analytics (Phase 3)")
    
    
    try:
        rm = RiskManager()
        var_95, es_95 = rm.calculate_market_risk()
        
        st.metric("Value at Risk (95%)", f"{var_95:.4%}", delta_color="inverse")
        st.metric("Expected Shortfall", f"{es_95:.4%}", delta_color="inverse")
        
        st.info("Risk metrics calculated from Phase 2 historical simulation.")
        
    except Exception as e:
        st.error(f"Could not load Risk Module. Run simulation.py first. Error: {e}")


st.subheader("Trade Tape")
if st.session_state.engine.trades:
    trade_df = pd.DataFrame(st.session_state.engine.trades)
    st.dataframe(trade_df.tail(10)) # Show last 10 trades
else:
    st.text("No trades executed yet.")