# Hypurr

A collection of cryptocurrency monitoring and trading tools.

## Tools Included

1. **Bitcoin Price Fetcher** - Retrieves real-time Bitcoin prices from CoinGecko API
2. **Hyperliquid Position Monitor** - Monitors Hyperliquid trading positions and sends Telegram notifications

---

## Bitcoin Price Fetcher

### Features

- Fetches real-time Bitcoin prices in multiple currencies (USD, EUR, GBP)
- Displays 24-hour price change percentage
- Shows Bitcoin market capitalization
- Clean, formatted output
- Error handling for network issues

### Installation

```bash
pip install -r requirements.txt
```

### Usage

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

### API

This script uses the [CoinGecko API](https://www.coingecko.com/en/api), which is free and doesn't require authentication for basic requests.

---

## Hyperliquid Position Monitor

A real-time monitoring tool that tracks Hyperliquid trading positions and sends instant Telegram notifications when positions or trades change.

### Features

- Real-time monitoring of Hyperliquid positions and trades
- Instant Telegram notifications for:
  - New positions opened
  - Positions closed
  - Position size changes
  - New trades executed
- Configurable check interval (default: 5 minutes)
- Support for both mainnet and testnet
- Comprehensive logging
- Easy configuration via environment variables

### Quick Start

1. **Set up a Telegram bot** (see [SETUP.md](SETUP.md) for detailed instructions):
   - Message @BotFather on Telegram
   - Create a new bot with `/newbot`
   - Save your bot token
   - Get your chat ID from @userinfobot

2. **Configure the monitor**:
   ```bash
   # Copy the example configuration
   cp .env.example .env

   # Edit .env with your values
   nano .env
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the monitor**:
   ```bash
   # Set environment variables
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   export TELEGRAM_CHAT_ID="your_chat_id_here"

   # Start monitoring
   python3 hyperliquid_monitor.py
   ```

### Configuration Options

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token (required)
- `TELEGRAM_CHAT_ID` - Your Telegram chat ID (required)
- `HYPERLIQUID_ADDRESS` - Address to monitor (default: 0xcb58b8f5ec6d47985f0728465c25a08ef9ad2c7b)
- `USE_TESTNET` - Use testnet instead of mainnet (default: false)
- `CHECK_INTERVAL` - Check interval in seconds (default: 300)

### Detailed Setup

See [SETUP.md](SETUP.md) for comprehensive setup instructions including:
- Step-by-step Telegram bot creation
- Multiple deployment methods (systemd, Docker, screen, nohup)
- Troubleshooting guide
- Security best practices

### Example Notifications

You'll receive formatted Telegram messages like:

```
🔔 POSITION OPENED

Asset: BTC
Side: LONG
Size: 0.5
Entry Price: $43,250.00
Leverage: 5x
Position Value: $21,625.00
Unrealized PnL: $0.00

Address: 0xcb58b8...ad2c7b
Time: 2025-12-30 12:00:00 UTC
```

```
🟢 NEW TRADE

Asset: BTC
Side: BUY
Price: $43,250.00
Size: 0.5
Fee: $2.16

Address: 0xcb58b8...ad2c7b
Time: 2025-12-30 12:00:00 UTC
```

### Running as a Background Service

For continuous monitoring, see [SETUP.md](SETUP.md) for instructions on running as:
- systemd service (Linux)
- Docker container
- screen/tmux session
- nohup background process

---

## Requirements

- Python 3.8 or higher
- Dependencies listed in requirements.txt:
  - requests
  - hyperliquid-python-sdk

## Installation

```bash
# Clone the repository
git clone https://github.com/milady0/Hypurr.git
cd Hypurr

# Install dependencies
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

MIT License - See LICENSE file for details