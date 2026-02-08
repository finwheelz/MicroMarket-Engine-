# Liquid-Risk: Institutional Market Microstructure & Risk Engine

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![ML](https://img.shields.io/badge/AI-Scikit--Learn-orange)
![Status](https://img.shields.io/badge/Status-Complete-green)

![Dashboard Screenshot](image_7b857b.png)

**Liquid-Risk** is a high-fidelity Market Microstructure Engine designed to simulate the full lifecycle of algorithmic trading. Unlike standard backtesters that assume infinite liquidity, this project simulates a realistic **Central Limit Order Book (CLOB)** to quantify slippage, market impact, and adverse selection.

## 🚀 Project Overview

The platform consists of three integrated layers:
1.  **Core Matching Engine (Phase 1):** Enforces **Price-Time Priority** and replicates exchange-level liquidity dynamics.
2.  **Quant-AI Layer (Phase 2):** Utilizes **Random Forest** classifiers to detect "toxic" order flow and prevent adverse selection.
3.  **FinTech Dashboard (Phase 3 & 4):** A real-time GUI providing visualization of **Value-at-Risk (VaR)**, **Expected Shortfall (ES)**, and live Order Book depth.

---

## 🛠️ Key Features

### 1. The Core Matching Engine (Microstructure)
* **Deterministic CLOB:** Implemented separate, sorted collections for Bids and Asks to ensure **O(1)** access to the Best Bid and Offer (BBO).
* **Price-Time Priority:** Enforces standard exchange matching logic (FIFO) where earlier orders at the same price are filled first.
* **Transaction Cost Analysis (TCA):** Calculates **Implementation Shortfall** by measuring the delta between Arrival Price and the actual VWAP of the execution.

### 2. AI-Driven Toxicity Detection (Quant Research)
* **Adverse Selection Model:** Trained a **Random Forest Classifier** on 5,000 simulated trading cycles to detect informed trading activity.
* **Feature Engineering:** Engineered **Order Flow Imbalance (OFI)** and Spread Width features to predict short-term volatility with **83% Precision**.
* **Dynamic Labeling:** Labels market states as "Toxic" (1) or "Safe" (0) based on future price movement horizons.

### 3. Institutional Risk Management
* **Tail Risk Metrics:** Implemented **Historical Value-at-Risk (VaR)** and **Expected Shortfall (ES/CVaR)** to quantify losses in the worst 5% of scenarios.
* **Stress Testing:** Includes a "Black Swan" simulator that artificially drains 80% of order book liquidity to measure portfolio drawdown during flash crashes.

### 4. Interactive Dashboard
* **Real-Time Visualization:** Built with **Streamlit** and **Plotly** to render Level 2 Market Depth (Bids vs. Asks) dynamically.
* **Live Execution:** Allows users to place Market and Limit orders to interact with the engine and observe immediate spread impact.

---

## 💻 Tech Stack
* **Language:** Python
* **Data & Math:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn
* **Visualization:** Streamlit, Plotly, Matplotlib

---
<img width="1901" height="880" alt="image" src="https://github.com/user-attachments/assets/1e66c6d1-8e05-4adb-8b71-785de0735107" />


