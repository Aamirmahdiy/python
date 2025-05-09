
import asyncio
import requests
from telegram import Bot
import time

# === Configuration ===
TOKEN = 'your bot token'
CHAT_ID = 'the ID of the channel you want the bot tosend the price to'  
CRYPTO = 'name of the crypto token'
CURRENCY = 'usd'

bot = Bot(token=TOKEN)

# === Function to get price from CoinGecko ===
def get_price():
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={CRYPTO}&vs_currencies={CURRENCY}'
    try:
        response = requests.get(url)
        data = response.json()
        price = data[CRYPTO][CURRENCY]
        return price
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

# === Async loop to send message every minute ===
async def send_price_loop():
    while True:
        price = get_price()
        if price:
            message = f"$ {price:,}"
            try:
                await bot.send_message(chat_id=CHAT_ID, text=message)
                print("✅ Sent:", message)
            except Exception as e:
                print("❌ Telegram error:", e)
        await asyncio.sleep(120)  # wait 120 seconds

# === Entry point ===
if __name__ == '__main__':
    asyncio.run(send_price_loop())

