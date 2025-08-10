import os
import time
import logging
from telegram import Bot
from telegram.error import TelegramError

# ✅ Get from environment (more secure)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
USER_ID = os.getenv('USER_ID')

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_TOKEN)

logging.basicConfig(level=logging.INFO)

# --- Configurable Parameters ---
MIN_LIQUIDITY = 30000   # Minimum liquidity in USD
MIN_VOLUME = 10000      # Minimum volume in USD in last 5 min
RISK_SCORE_THRESHOLD = 70  # Minimum risk score to send alert

# Dummy function to simulate memecoin data (replace with real API later)
def fetch_trending_memecoins():
    return [
        {
            'symbol': 'MOONCAT',
            'price': 0.000023,
            'volume_5m': 45000,
            'liquidity': 80000,
            'market_cap': 150000,
            'rug_check_passed': True,
            'honeypot_passed': True,
            'risk_score': 85,
            'buy_signal': True,
            'sell_signal': False
        },
        {
            'symbol': 'RUGME',
            'price': 0.000001,
            'volume_5m': 1200,
            'liquidity': 500,
            'market_cap': 10000,
            'rug_check_passed': False,
            'honeypot_passed': False,
            'risk_score': 10,
            'buy_signal': False,
            'sell_signal': False
        }
    ]

# Format and send alert to Telegram
def send_telegram_message(text):
    try:
        bot.send_message(chat_id=USER_ID, text=text, parse_mode='Markdown')
    except TelegramError as e:
        logging.error(f"Telegram send failed: {e}")

def format_signal_message(token):
    signal = "BUY 🚀" if token['buy_signal'] else "SELL 🔻" if token['sell_signal'] else "HOLD ⏸️"
    return f"""
🔥 *{signal} SIGNAL*: {token['symbol']}

💰 Price: ${token['price']:.8f}
📊 5-min Volume: ${token['volume_5m']:,}
💧 Liquidity: ${token['liquidity']:,}
📈 Market Cap: ${token['market_cap']:,}
🛡️ Rug Check: {'Passed' if token['rug_check_passed'] else 'Failed'}
🐝 Honeypot: {'Passed' if token['honeypot_passed'] else 'Failed'}
⚠️ Risk Score: {token['risk_score']}/100

➡️ Suggested Action: *{signal}*
"""

def main():
    logging.info("🚀 Solana Memecoin Bot Started")
    while True:
        try:
            tokens = fetch_trending_memecoins()
            for token in tokens:
                if (
                    token['risk_score'] >= RISK_SCORE_THRESHOLD and
                    token['rug_check_passed'] and
                    token['honeypot_passed']
                ):
                    msg = format_signal_message(token)
                    send_telegram_message(msg)
                    logging.info(f"✅ Alert sent for {token['symbol']}")
            time.sleep(300)  # Wait 5 minutes before next scan
        except Exception as e:
            logging.error(f"⚠️ Error: {e}")
            time.sleep(60)

if __name__ == '__main__':
    main()