# Liquid-Risk: Institutional Market Microstructure & Risk Engine

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![ML](https://img.shields.io/badge/AI-Scikit--Learn-orange)
![Status](https://img.shields.io/badge/Status-Complete-green)

[cite_start]**Liquid-Risk** is a high-fidelity Market Microstructure Engine designed to simulate the full lifecycle of algorithmic trading[cite: 4]. [cite_start]Unlike standard backtesters that assume infinite liquidity, this project simulates a realistic **Central Limit Order Book (CLOB)** to quantify slippage, market impact, and adverse selection[cite: 12, 24].

## 🚀 Project Overview

The platform consists of three integrated layers:
1.  [cite_start]**Core Matching Engine (Phase 1):** Enforces **Price-Time Priority** and replicates exchange-level liquidity dynamics[cite: 5].
2.  [cite_start]**Quant-AI Layer (Phase 2):** Utilizes **Random Forest** classifiers to detect "toxic" order flow and prevent adverse selection[cite: 6].
3.  [cite_start]**FinTech Dashboard (Phase 3 & 4):** A real-time GUI providing visualization of **Value-at-Risk (VaR)**, **Expected Shortfall (ES)**, and live Order Book depth[cite: 7].

---

## 🛠️ Key Features

### 1. The Core Matching Engine (Microstructure)
* [cite_start]**Deterministic CLOB:** Implemented separate, sorted collections for Bids and Asks to ensure **O(1)** access to the Best Bid and Offer (BBO)[cite: 14, 15].
* [cite_start]**Price-Time Priority:** Enforces standard exchange matching logic (FIFO) where earlier orders at the same price are filled first[cite: 17, 30].
* [cite_start]**Transaction Cost Analysis (TCA):** Calculates **Implementation Shortfall** by measuring the delta between Arrival Price and the actual VWAP of the execution[cite: 24, 56].

### 2. AI-Driven Toxicity Detection (Quant Research)
* [cite_start]**Adverse Selection Model:** Trained a **Random Forest Classifier** on 5,000 simulated trading cycles to detect informed trading activity[cite: 38, 47].
* [cite_start]**Feature Engineering:** Engineered **Order Flow Imbalance (OFI)** and Spread Width features to predict short-term volatility with **83% Precision**[cite: 42, 48].
* [cite_start]**Dynamic Labeling:** Labels market states as "Toxic" (1) or "Safe" (0) based on future price movement horizons[cite: 44, 45].

### 3. Institutional Risk Management
* [cite_start]**Tail Risk Metrics:** Implemented **Historical Value-at-Risk (VaR)** and **Expected Shortfall (ES/CVaR)** to quantify losses in the worst 5% of scenarios[cite: 52].
* [cite_start]**Stress Testing:** Includes a "Black Swan" simulator that artificially drains 80% of order book liquidity to measure portfolio drawdown during flash crashes[cite: 54].

### 4. Interactive Dashboard
* [cite_start]**Real-Time Visualization:** Built with **Streamlit** and **Plotly** to render Level 2 Market Depth (Bids vs. Asks) dynamically[cite: 60].
* [cite_start]**Live Execution:** Allows users to place Market and Limit orders to interact with the engine and observe immediate spread impact[cite: 62].

---

## 💻 Tech Stack
* **Language:** Python
* **Data & Math:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn
* **Visualization:** Streamlit, Plotly, Matplotlib

---

## 📸 Installation & Usage

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/yourusername/liquid-risk.git](https://github.com/yourusername/liquid-risk.git)
   cd liquid-risk
