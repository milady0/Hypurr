# Hyperliquid Position Monitor - Setup Guide

This guide will walk you through setting up the Hyperliquid position monitor with Telegram notifications.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Creating a Telegram Bot](#creating-a-telegram-bot)
3. [Getting Your Telegram Chat ID](#getting-your-telegram-chat-id)
4. [Installing Dependencies](#installing-dependencies)
5. [Configuration](#configuration)
6. [Running the Monitor](#running-the-monitor)
7. [Running as a Background Service](#running-as-a-background-service)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.8 or higher
- A Telegram account
- Internet connection
- Linux/macOS/Windows with Python installed

---

## Creating a Telegram Bot

Follow these steps to create your own Telegram bot:

### Step 1: Open Telegram and Find BotFather

1. Open Telegram on your device
2. Search for `@BotFather` (this is the official Telegram bot for creating bots)
3. Start a chat with BotFather

### Step 2: Create a New Bot

1. Send the command `/newbot` to BotFather
2. BotFather will ask you to choose a name for your bot (e.g., "Hyperliquid Monitor")
3. Then choose a username for your bot (must end with 'bot', e.g., "hyperliquid_alerts_bot")

### Step 3: Save Your Bot Token

After creating the bot, BotFather will send you a message containing your bot token. It looks like this:

```
123456789:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
```

**IMPORTANT:** Keep this token secure! Anyone with this token can control your bot.

Copy this token - you'll need it for the configuration step.

---

## Getting Your Telegram Chat ID

You need to get your chat ID so the bot knows where to send messages.

### Method 1: Using the GetIDs Bot (Easiest)

1. Search for `@userinfobot` in Telegram
2. Start a chat and send any message
3. The bot will reply with your user information, including your Chat ID
4. Copy the `Id` number (it will look like `123456789`)

### Method 2: Using the Web Method

1. Send a message to your newly created bot (just type `/start`)
2. Open your browser and go to:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
   Replace `<YOUR_BOT_TOKEN>` with your actual bot token

3. Look for the `"chat":{"id":` field in the JSON response
4. The number after `"id":` is your chat ID

Example response:
```json
{
  "ok": true,
  "result": [{
    "message": {
      "chat": {
        "id": 123456789,  <-- This is your chat ID
        "first_name": "Your Name"
      }
    }
  }]
}
```

---

## Installing Dependencies

### Step 1: Clone or Download the Repository

If you haven't already, get the code:

```bash
git clone https://github.com/milady0/Hypurr.git
cd Hypurr
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - for HTTP requests
- `hyperliquid-python-sdk` - official Hyperliquid API SDK

---

## Configuration

You can configure the monitor using environment variables. There are two methods:

### Method 1: Using a .env File (Recommended)

Create a `.env` file in the project directory:

```bash
nano .env  # or use your favorite text editor
```

Add the following content (replace with your actual values):

```bash
# Required: Your Telegram bot token from BotFather
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890

# Required: Your Telegram chat ID
TELEGRAM_CHAT_ID=123456789

# Optional: Hyperliquid address to monitor (defaults to the one in the task)
HYPERLIQUID_ADDRESS=0xcb58b8f5ec6d47985f0728465c25a08ef9ad2c7b

# Optional: Use testnet instead of mainnet (default: false)
USE_TESTNET=false

# Optional: Check interval in seconds (default: 300 = 5 minutes)
CHECK_INTERVAL=300
```

Save the file and exit.

To use the .env file, you'll need to load it when running the script:

```bash
# Install python-dotenv
pip install python-dotenv

# Then modify the script to load .env (or use the command below)
```

### Method 2: Export Environment Variables Directly

Set the environment variables in your terminal:

```bash
export TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890"
export TELEGRAM_CHAT_ID="123456789"
export HYPERLIQUID_ADDRESS="0xcb58b8f5ec6d47985f0728465c25a08ef9ad2c7b"
export CHECK_INTERVAL="300"
```

On Windows (Command Prompt):
```cmd
set TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
set TELEGRAM_CHAT_ID=123456789
set HYPERLIQUID_ADDRESS=0xcb58b8f5ec6d47985f0728465c25a08ef9ad2c7b
set CHECK_INTERVAL=300
```

---

## Running the Monitor

### Basic Usage

Once configured, simply run:

```bash
python3 hyperliquid_monitor.py
```

You should see output like:
```
2025-12-30 12:00:00 - INFO - Initialized monitor for address: 0xcb58b8f5ec6d47985f0728465c25a08ef9ad2c7b
2025-12-30 12:00:00 - INFO - Using mainnet API
2025-12-30 12:00:00 - INFO - Starting monitor with 300s interval
2025-12-30 12:00:00 - INFO - Running monitoring check...
```

And you should receive a Telegram message confirming monitoring has started!

### Using with .env File

If you created a .env file:

```bash
# Install python-dotenv if you haven't
pip install python-dotenv

# Run with environment variable loading
python3 -c "from dotenv import load_dotenv; load_dotenv()" && python3 hyperliquid_monitor.py
```

Or create a simple launcher script `run_monitor.sh`:

```bash
#!/bin/bash
source venv/bin/activate
set -a
source .env
set +a
python3 hyperliquid_monitor.py
```

Make it executable and run:
```bash
chmod +x run_monitor.sh
./run_monitor.sh
```

### Stopping the Monitor

Press `Ctrl+C` to stop the monitor. You'll receive a Telegram notification that monitoring has stopped.

---

## Running as a Background Service

For continuous monitoring, you'll want to run the script as a service.

### Method 1: Using Screen (Linux/macOS)

```bash
# Install screen if not available
sudo apt-get install screen  # Ubuntu/Debian
# or
brew install screen  # macOS

# Start a new screen session
screen -S hyperliquid_monitor

# Activate virtual environment and run
source venv/bin/activate
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
python3 hyperliquid_monitor.py

# Detach from screen: Press Ctrl+A, then D

# To reattach later:
screen -r hyperliquid_monitor

# To list all screens:
screen -ls
```

### Method 2: Using nohup (Linux/macOS)

```bash
# Set environment variables first
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"

# Run with nohup
nohup python3 hyperliquid_monitor.py > monitor.log 2>&1 &

# Check if it's running
ps aux | grep hyperliquid_monitor

# View logs
tail -f monitor.log

# To stop, find the process ID and kill it
ps aux | grep hyperliquid_monitor
kill <PID>
```

### Method 3: Using systemd (Linux)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/hyperliquid-monitor.service
```

Add the following content (adjust paths as needed):

```ini
[Unit]
Description=Hyperliquid Position Monitor
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/Hypurr
Environment="TELEGRAM_BOT_TOKEN=your_token_here"
Environment="TELEGRAM_CHAT_ID=your_chat_id_here"
Environment="HYPERLIQUID_ADDRESS=0xcb58b8f5ec6d47985f0728465c25a08ef9ad2c7b"
ExecStart=/path/to/Hypurr/venv/bin/python3 /path/to/Hypurr/hyperliquid_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable hyperliquid-monitor

# Start the service
sudo systemctl start hyperliquid-monitor

# Check status
sudo systemctl status hyperliquid-monitor

# View logs
sudo journalctl -u hyperliquid-monitor -f

# Stop the service
sudo systemctl stop hyperliquid-monitor
```

### Method 4: Using Docker (Advanced)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY hyperliquid_monitor.py .

CMD ["python", "hyperliquid_monitor.py"]
```

Build and run:

```bash
# Build image
docker build -t hyperliquid-monitor .

# Run container
docker run -d \
  --name hyperliquid-monitor \
  --restart unless-stopped \
  -e TELEGRAM_BOT_TOKEN="your_token_here" \
  -e TELEGRAM_CHAT_ID="your_chat_id_here" \
  -e HYPERLIQUID_ADDRESS="0xcb58b8f5ec6d47985f0728465c25a08ef9ad2c7b" \
  hyperliquid-monitor

# View logs
docker logs -f hyperliquid-monitor

# Stop container
docker stop hyperliquid-monitor
```

---

## Troubleshooting

### Issue: "TELEGRAM_BOT_TOKEN environment variable not set"

**Solution:** Make sure you've set the environment variable before running the script:
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
```

### Issue: "Failed to send Telegram notification"

**Possible causes:**
1. Invalid bot token - double-check the token from BotFather
2. Invalid chat ID - verify you're using the correct chat ID
3. Bot wasn't started - send `/start` to your bot in Telegram first
4. Network issues - check your internet connection

**Solution:** Test your bot token manually:
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe"
```

### Issue: "Error fetching user state" or "Error fetching user fills"

**Possible causes:**
1. Invalid Hyperliquid address
2. Network issues
3. API rate limiting

**Solution:**
- Verify the address is correct
- Check the logs in `hyperliquid_monitor.log`
- Try increasing the CHECK_INTERVAL to reduce API calls

### Issue: Script stops unexpectedly

**Solution:**
- Check the log file: `cat hyperliquid_monitor.log`
- Run as a background service (see above)
- Enable restart on failure (systemd or Docker)

### Issue: Not receiving notifications for changes

**Possible causes:**
1. No actual changes occurred
2. Check interval is too long
3. Script not detecting changes properly

**Solution:**
- Check the log file to see if changes were detected
- Reduce CHECK_INTERVAL for more frequent checks
- Make a test trade to verify notifications work

### Issue: Too many notifications

**Solution:** The script only notifies on actual changes. If you're getting too many notifications:
- The address might be very active
- Consider filtering by position size or specific coins (requires code modification)

---

## Getting Help

If you encounter issues:

1. Check the log file: `hyperliquid_monitor.log`
2. Verify all environment variables are set correctly
3. Test the Telegram bot independently
4. Check the Hyperliquid API status

For more information:
- Hyperliquid API Documentation: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api
- Telegram Bot API: https://core.telegram.org/bots/api
- Python SDK: https://github.com/hyperliquid-dex/hyperliquid-python-sdk

---

## Security Notes

1. **Never share your bot token** - treat it like a password
2. **Keep your .env file private** - add it to `.gitignore`
3. **Use environment variables** for sensitive data
4. **Regularly rotate your bot token** if you suspect it's been compromised

To regenerate your bot token:
1. Message @BotFather
2. Send `/token`
3. Select your bot
4. Follow the instructions to generate a new token

---

## What You'll Be Notified About

Once running, you'll receive Telegram notifications for:

- ✅ **Monitoring started** - Confirmation when the script starts
- 🟢 **New trades** - When a buy order is filled
- 🔴 **New trades** - When a sell order is filled
- 🔔 **Position opened** - When a new position is created
- 🔔 **Position modified** - When position size changes
- 🔵 **Position closed** - When a position is fully closed
- ⚠️ **Monitoring stopped** - When you stop the script
- ❌ **Errors** - If the script encounters a fatal error

Each notification includes relevant details like asset, price, size, leverage, and timestamp.

---

Enjoy monitoring your Hyperliquid positions! 🚀
