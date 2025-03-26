import re
import time
from pyrogram import Client, filters

API_ID = "26592308"  # Replace with your API ID
API_HASH = "a2e265097c7b2cc34e2d893707e2e56f"  # Replace with your API Hash

# Initialize the user client
app = Client("telegram_user.session", api_id=API_ID, api_hash=API_HASH)

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
                # Send the three messages with a delay
                messages = [
                    "Hey there! How are you?",
                    "I am Enkli from LanderLab, your Dedicated Account Manager.",
                    "Please do not hesitate to contact me here if you have any question or need help."
                ]
                for msg in messages:
                    client.send_message(username, msg)
                    print(f"✅ Message sent to @{username}: {msg}")
                    time.sleep(5)  # Wait for 5 seconds before sending the next message

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
            app.storage.delete()  # Proper session cleanup
            run_bot()

# Start bot
run_bot()
