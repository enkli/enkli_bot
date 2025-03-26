import re
import time
from pyrogram import Client, filters

API_ID = "26592308"
API_HASH = "a2e265097c7b2cc34e2d893707e2e56f" 

# Initialize the user client
app = Client("telegram_user", api_id=API_ID, api_hash=API_HASH)

USERNAME_PATTERN = r"Phone Number:\s*telegram\s*-\s*([\w\d_]+)"

def log_error(error_message):
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")
    print(f"❌ ERROR: {error_message}")

@app.on_message(filters.group & filters.text)
def check_message(client, message):
    try:
        text = message.text
        print(f"📩 New message in group: {text}")

        match = re.search(USERNAME_PATTERN, text)
        if match:
            username = match.group(1)
            print(f"🔍 Found Telegram username: @{username}")

            try:
                client.send_message(username, "Hey there! 👋")
                print(f"✅ Message sent to @{username}")
            except Exception as e:
                log_error(f"Could not send message to @{username}: {e}")

    except Exception as e:
        log_error(f"Error processing message: {e}")

def run_bot():
    try:
        print("🤖 User Bot is starting...")
        app.run()
    except Exception as e:
        log_error(f"User Bot failed to start: {e}")
        if "SESSION_REVOKED" in str(e):
            print("❌ Session revoked. Deleting session and trying again.")
            app.delete_session()
            run_bot()

# Start bot
run_bot()
