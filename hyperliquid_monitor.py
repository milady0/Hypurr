#!/usr/bin/env python3
"""
Hyperliquid Position Monitor
Monitors a Hyperliquid address for position and trade changes and sends Telegram notifications.
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set
import requests
from hyperliquid.info import Info
from hyperliquid.utils import constants

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hyperliquid_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Handles sending notifications via Telegram."""

    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram notifier.

        Args:
            bot_token: Telegram bot token from BotFather
            chat_id: Chat ID to send messages to
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def send_message(self, message: str) -> bool:
        """
        Send a message via Telegram.

        Args:
            message: Message text to send

        Returns:
            True if successful, False otherwise
        """
        try:
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Telegram notification sent successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False


class HyperliquidMonitor:
    """Monitors Hyperliquid positions and trades for a specific address."""

    def __init__(self, address: str, telegram_notifier: TelegramNotifier, use_testnet: bool = False):
        """
        Initialize the monitor.

        Args:
            address: Hyperliquid address to monitor
            telegram_notifier: TelegramNotifier instance
            use_testnet: Whether to use testnet (default: False for mainnet)
        """
        self.address = address
        self.notifier = telegram_notifier
        api_url = constants.TESTNET_API_URL if use_testnet else constants.MAINNET_API_URL
        self.info = Info(api_url, skip_ws=True)

        # State tracking
        self.previous_positions: Dict = {}
        self.previous_fills_ids: Set[str] = set()
        self.is_first_run = True

        logger.info(f"Initialized monitor for address: {address}")
        logger.info(f"Using {'testnet' if use_testnet else 'mainnet'} API")

    def get_user_state(self) -> Optional[Dict]:
        """
        Fetch current user state (positions).

        Returns:
            User state dict or None if error
        """
        try:
            state = self.info.user_state(self.address)
            return state
        except Exception as e:
            logger.error(f"Error fetching user state: {e}")
            return None

    def get_user_fills(self) -> Optional[List[Dict]]:
        """
        Fetch recent user fills (trades).

        Returns:
            List of fills or None if error
        """
        try:
            fills = self.info.user_fills(self.address)
            return fills
        except Exception as e:
            logger.error(f"Error fetching user fills: {e}")
            return None

    def format_position_message(self, coin: str, position: Dict, action: str) -> str:
        """
        Format a position change message.

        Args:
            coin: Asset symbol
            position: Position data
            action: Type of change (opened, closed, modified)

        Returns:
            Formatted message string
        """
        leverage = position.get('leverage', {}).get('value', 'N/A')
        size = position.get('szi', 'N/A')
        entry_px = position.get('entryPx', 'N/A')
        position_value = position.get('positionValue', 'N/A')
        unrealized_pnl = position.get('unrealizedPnl', 'N/A')

        side = "LONG" if float(size) > 0 else "SHORT" if float(size) < 0 else "NEUTRAL"

        message = f"🔔 <b>Position {action.upper()}</b>\n\n"
        message += f"<b>Asset:</b> {coin}\n"
        message += f"<b>Side:</b> {side}\n"
        message += f"<b>Size:</b> {abs(float(size))}\n"
        message += f"<b>Entry Price:</b> ${entry_px}\n"
        message += f"<b>Leverage:</b> {leverage}x\n"
        message += f"<b>Position Value:</b> ${position_value}\n"
        message += f"<b>Unrealized PnL:</b> ${unrealized_pnl}\n"
        message += f"\n<b>Address:</b> <code>{self.address[:8]}...{self.address[-6:]}</code>"
        message += f"\n<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"

        return message

    def format_fill_message(self, fill: Dict) -> str:
        """
        Format a trade/fill message.

        Args:
            fill: Fill data

        Returns:
            Formatted message string
        """
        coin = fill.get('coin', 'N/A')
        side = fill.get('side', 'N/A')
        px = fill.get('px', 'N/A')
        sz = fill.get('sz', 'N/A')
        fee = fill.get('fee', 'N/A')
        time_ms = fill.get('time', 0)
        tid = fill.get('tid', 'N/A')

        # Convert timestamp
        time_str = datetime.fromtimestamp(time_ms / 1000).strftime('%Y-%m-%d %H:%M:%S UTC')

        emoji = "🟢" if side.lower() == "buy" else "🔴"

        message = f"{emoji} <b>NEW TRADE</b>\n\n"
        message += f"<b>Asset:</b> {coin}\n"
        message += f"<b>Side:</b> {side.upper()}\n"
        message += f"<b>Price:</b> ${px}\n"
        message += f"<b>Size:</b> {sz}\n"
        message += f"<b>Fee:</b> ${fee}\n"
        message += f"<b>Trade ID:</b> <code>{tid}</code>\n"
        message += f"\n<b>Address:</b> <code>{self.address[:8]}...{self.address[-6:]}</code>"
        message += f"\n<b>Time:</b> {time_str}"

        return message

    def check_positions(self, current_state: Dict) -> None:
        """
        Check for position changes and send notifications.

        Args:
            current_state: Current user state from API
        """
        if not current_state or 'assetPositions' not in current_state:
            return

        current_positions = {}

        # Build current positions dict
        for position in current_state['assetPositions']:
            coin = position['position']['coin']
            current_positions[coin] = position['position']

        # Skip notifications on first run
        if self.is_first_run:
            self.previous_positions = current_positions
            logger.info(f"Initial state: {len(current_positions)} positions found")
            return

        # Check for new or modified positions
        for coin, position in current_positions.items():
            if coin not in self.previous_positions:
                # New position opened
                message = self.format_position_message(coin, position, "opened")
                self.notifier.send_message(message)
                logger.info(f"New position opened: {coin}")
            else:
                # Check if position size changed
                old_size = float(self.previous_positions[coin].get('szi', 0))
                new_size = float(position.get('szi', 0))

                if abs(old_size - new_size) > 0.0001:  # Account for floating point precision
                    message = self.format_position_message(coin, position, "modified")
                    self.notifier.send_message(message)
                    logger.info(f"Position modified: {coin} (old: {old_size}, new: {new_size})")

        # Check for closed positions
        for coin in self.previous_positions:
            if coin not in current_positions:
                # Position closed
                old_position = self.previous_positions[coin]
                message = f"🔵 <b>Position CLOSED</b>\n\n"
                message += f"<b>Asset:</b> {coin}\n"
                message += f"<b>Previous Size:</b> {old_position.get('szi', 'N/A')}\n"
                message += f"\n<b>Address:</b> <code>{self.address[:8]}...{self.address[-6:]}</code>"
                message += f"\n<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"

                self.notifier.send_message(message)
                logger.info(f"Position closed: {coin}")

        # Update previous positions
        self.previous_positions = current_positions

    def check_fills(self, current_fills: List[Dict]) -> None:
        """
        Check for new trades/fills and send notifications.

        Args:
            current_fills: List of recent fills from API
        """
        if not current_fills:
            return

        # Build set of current fill IDs
        current_fill_ids = set()
        for fill in current_fills:
            tid = fill.get('tid')
            if tid:
                current_fill_ids.add(str(tid))

        # Skip notifications on first run
        if self.is_first_run:
            self.previous_fills_ids = current_fill_ids
            logger.info(f"Initial state: {len(current_fill_ids)} recent fills found")
            return

        # Find new fills
        new_fill_ids = current_fill_ids - self.previous_fills_ids

        if new_fill_ids:
            # Send notification for each new fill
            for fill in current_fills:
                tid = str(fill.get('tid', ''))
                if tid in new_fill_ids:
                    message = self.format_fill_message(fill)
                    self.notifier.send_message(message)
                    logger.info(f"New fill detected: {tid}")

        # Update previous fills
        self.previous_fills_ids = current_fill_ids

    def run_check(self) -> None:
        """Run a single monitoring check."""
        logger.info("Running monitoring check...")

        # Check positions
        user_state = self.get_user_state()
        if user_state:
            self.check_positions(user_state)

        # Check fills
        user_fills = self.get_user_fills()
        if user_fills:
            self.check_fills(user_fills)

        # Mark first run as complete
        if self.is_first_run:
            self.is_first_run = False
            self.notifier.send_message(
                f"✅ <b>Monitoring Started</b>\n\n"
                f"Now monitoring address:\n<code>{self.address}</code>\n\n"
                f"You will receive notifications for:\n"
                f"• New positions opened\n"
                f"• Positions closed\n"
                f"• Position size changes\n"
                f"• New trades executed"
            )

    def start(self, interval_seconds: int = 300) -> None:
        """
        Start the monitoring loop.

        Args:
            interval_seconds: Check interval in seconds (default: 300 = 5 minutes)
        """
        logger.info(f"Starting monitor with {interval_seconds}s interval")

        try:
            while True:
                self.run_check()
                logger.info(f"Sleeping for {interval_seconds} seconds...")
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            logger.info("Monitor stopped by user")
            self.notifier.send_message("⚠️ <b>Monitoring Stopped</b>")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            self.notifier.send_message(f"❌ <b>Monitor Error</b>\n\n{str(e)}")
            raise


def main():
    """Main entry point."""
    # Load configuration from environment variables
    ADDRESS = os.getenv('HYPERLIQUID_ADDRESS', '0xcb58b8f5ec6d47985f0728465c25a08ef9ad2c7b')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    USE_TESTNET = os.getenv('USE_TESTNET', 'false').lower() == 'true'
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '300'))  # Default 5 minutes

    # Validate configuration
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        sys.exit(1)

    if not TELEGRAM_CHAT_ID:
        logger.error("TELEGRAM_CHAT_ID environment variable not set")
        sys.exit(1)

    # Initialize notifier
    notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

    # Initialize monitor
    monitor = HyperliquidMonitor(ADDRESS, notifier, USE_TESTNET)

    # Start monitoring
    monitor.start(CHECK_INTERVAL)


if __name__ == '__main__':
    main()
