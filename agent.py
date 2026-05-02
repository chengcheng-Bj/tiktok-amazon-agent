import os
import requests
import time

print("--- Agent Execution Started ---")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def ask_ai():
    # 2026年5月最新可用 ID，确保这一行有缩进
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview:generateContent?key={GEMINI_API_KEY}"
    
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    prompt = f"Give 1 unique trending Amazon product idea for TikTok selling. Be concise and professional. Context time: {current_time}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    for i in range(3):
        try:
            r = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            if r.status_code != 200:
                print(f"Attempt {i+1} - API Error {r.status_code}: {r.text}")
                time.sleep(5)
                continue

            data = r.json()

            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                parts = candidate.get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "Empty response text")
            
            print(f"Attempt {i+1} - Unexpected JSON structure: {data}")

        except Exception as e:
            print(f"Attempt {i+1} - Exception: {repr(e)}")
            time.sleep(2)

    return "AI ERROR: Failed to get response from Gemini 3.1"

def send_telegram(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram configuration missing!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            print("Successfully sent to Telegram")
        else:
            print(f"Telegram Failed: {response.text}")
    except Exception as e:
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    result = ask_ai()
    print(f"AI Result: {result}")
    send_telegram(result)
    print("--- Agent Execution Finished ---")

    
