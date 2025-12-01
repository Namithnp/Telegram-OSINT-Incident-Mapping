from pyrogram import Client

api_id = 36932811          # ← replace with your api_id
api_hash = "38f4b6e10f7e8fb2ce7543c5eb9966f0"  # ← replace with your api_hash

app = Client("my_account", api_id=api_id, api_hash=api_hash)

@app.on_message()
async def handler(client, message):
    print("MSG from:", message.chat.title or getattr(message.from_user, 'first_name', 'unknown'))
    print("Text:", message.text)

if __name__ == "__main__":
    print("Starting client...")
    app.run()
    print("Client stopped.")
