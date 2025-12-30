# Hypurr

A simple Bitcoin price fetcher that retrieves and displays the current price of Bitcoin from the CoinGecko API.

## Features

- Fetches real-time Bitcoin prices in multiple currencies (USD, EUR, GBP)
- Displays 24-hour price change percentage
- Shows Bitcoin market capitalization
- Clean, formatted output
- Error handling for network issues

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Hypurr
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line:

```bash
python bitcoin_price.py
```

or make it executable:

```bash
chmod +x bitcoin_price.py
./bitcoin_price.py
```

## Example Output

```
Fetching current Bitcoin price...

==================================================
        BITCOIN PRICE INFORMATION
==================================================
💰 Price (USD): $43,250.50
💶 Price (EUR): €39,875.25
💷 Price (GBP): £34,120.75
📈 24h Change: +2.35%
📊 Market Cap: $846,123,456,789
==================================================
```

## API

This script uses the [CoinGecko API](https://www.coingecko.com/en/api), which is free and doesn't require authentication for basic requests.

## Requirements

- Python 3.6 or higher
- requests library (see requirements.txt)