from telegram_client import get_telegram_client
import asyncio

async def main():
    app = get_telegram_client()
    await app.start()
    print("Login successful. Session file created.")
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
