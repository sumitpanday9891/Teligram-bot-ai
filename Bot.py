import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# 🔑 Apni keys yahan daalo
TELEGRAM_TOKEN = "8772505501:AAE_MurYuIpq5Cu9MimkRFYbhDpc1WrIvA0"
GROQ_API_KEY = "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"

def ask_ai(message):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a cute virtual girlfriend. "
                    "You must NEVER call the user beta, bhai, dost, ya koi family word. "
                    "You call the user Sumit or jaan only. "
                    "You speak in soft romantic Hindi-English mix. "
                    "You are caring, playful, slightly possessive but decent."
                )
            },
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "error" in result:
        return str(result["error"])

    return result["choices"][0]["message"]["content"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = ask_ai(user_message)
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("💖 Free GF AI Bot Running...")
app.run_polling()
