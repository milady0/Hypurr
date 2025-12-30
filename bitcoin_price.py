#!/usr/bin/env python3
"""
Bitcoin Price Fetcher
Fetches the current price of Bitcoin from the CoinGecko API and displays it.
"""

import requests
import json


def fetch_bitcoin_price():
    """
    Fetches the current Bitcoin price from CoinGecko API.

    Returns:
        dict: Dictionary containing price information or None if request fails
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd,eur,gbp",
        "include_24hr_change": "true",
        "include_market_cap": "true"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None


def display_price(data):
    """
    Displays the Bitcoin price information in a formatted way.

    Args:
        data (dict): Price data from the API
    """
    if not data or "bitcoin" not in data:
        print("Failed to retrieve Bitcoin price data.")
        return

    bitcoin_data = data["bitcoin"]

    print("\n" + "="*50)
    print("        BITCOIN PRICE INFORMATION")
    print("="*50)

    # Display prices
    if "usd" in bitcoin_data:
        usd_price = bitcoin_data["usd"]
        print(f"💰 Price (USD): ${usd_price:,.2f}")

    if "eur" in bitcoin_data:
        eur_price = bitcoin_data["eur"]
        print(f"💶 Price (EUR): €{eur_price:,.2f}")

    if "gbp" in bitcoin_data:
        gbp_price = bitcoin_data["gbp"]
        print(f"💷 Price (GBP): £{gbp_price:,.2f}")

    # Display 24-hour change
    if "usd_24h_change" in bitcoin_data:
        change = bitcoin_data["usd_24h_change"]
        change_symbol = "📈" if change > 0 else "📉"
        print(f"{change_symbol} 24h Change: {change:+.2f}%")

    # Display market cap
    if "usd_market_cap" in bitcoin_data:
        market_cap = bitcoin_data["usd_market_cap"]
        print(f"📊 Market Cap: ${market_cap:,.0f}")

    print("="*50 + "\n")


def main():
    """Main function to fetch and display Bitcoin price."""
    print("Fetching current Bitcoin price...")

    price_data = fetch_bitcoin_price()
    display_price(price_data)


if __name__ == "__main__":
    main()
