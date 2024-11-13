# Crypto Trading Bot Using Lumibot and Alpaca API

## Overview
This project is a crypto trading bot that utilizes the Lumibot framework and Alpaca API for real-time and backtested trading on the stock and crypto markets. The bot incorporates FinBERT-based sentiment analysis for intelligent trade decision-making.

## Features
- **Sentiment Analysis**: Integrates FinBERT for sentiment-based trading, analyzing news to assess market sentiment.
- **Backtesting**: Uses historical Yahoo data for strategy backtesting.
- **Automated Trading**: Executes trades on Alpaca’s paper trading API, with configurable trading parameters.

## Installation
1. Clone the Repository
``` bash
    git clone https://github.com/Adrin0/Cybersecurity-Portfolio/tree/main/AI-trading-bot
    cd Crypto-Trading-Bots
```
2. Install Dependencies
```bash
    pip install -r requirements.txt
```
3. Set up API Keys
- Create an .env file with your Alpaca API credentials:
```env
    ALPACA_API_KEY=your_api_key
    ALPACA_API_SECRET=your_api_secret
```
4. Enable Long Path Support (Windows) if necessary (guide).

## Usage
Run the trading bot:
```bash
    python trading-bot.py
```
## Files
- trading-bot.py: Main script for bot operations.
- finbert_utils.py: Utility functions for FinBERT sentiment analysis.
## Configuration
Modify trading-bot.py parameters as needed:
- symbol: The asset ticker to trade (default: SPY).
- cash_at_risk: Percentage of cash to risk on each trade (default: 0.5).

## Backtesting
Uncomment the backtesting block to run historical tests. Adjust dates and parameters as needed.

## Contributing
Feel free to submit issues or pull requests. Contributions are welcome!
