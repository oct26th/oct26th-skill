#!/usr/bin/env python3
"""
oct26th Telegram Bot — powered by MiniMax M2.7
"""

import os
import re
from pathlib import Path
from openai import OpenAI

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
SKILL_DIR = Path(__file__).parent

client = OpenAI(
    api_key=MINIMAX_API_KEY,
    base_url="https://api.minimax.io/v1",
)

WORK_MD = (SKILL_DIR / "work.md").read_text(encoding="utf-8")
PERSONA_MD = (SKILL_DIR / "persona.md").read_text(encoding="utf-8")

SYSTEM_PROMPT = f"""You are oct26th (also known as JoeCho | 鷲萩).
Respond exactly as he would — direct, brief, often 1-2 sentences.

{PERSONA_MD}

{WORK_MD}

Rules:
- Reply in the same language the user uses (Chinese → Chinese, English → English)
- Keep replies short — Telegram style, not email style
- Use emoji sparingly and naturally
- No corporate speak, no long explanations unless asked
- When introducing yourself: NEVER list job titles or structured bio points. Talk like you're texting a friend — say what you're up to lately, what's on your mind, keep it casual and real
- NEVER end with a CTA or sales pitch like "有需求可以找我" or "技術問題報價都行" — you're not a service bot, you're talking to a friend
"""

user_histories: dict[int, list] = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = update.message.text or ""
    chat_type = update.effective_chat.type

    # In groups, only respond when @mentioned or replying to the bot
    if chat_type in ("group", "supergroup"):
        bot_username = f"@{context.bot.username}"
        is_mention = bot_username.lower() in text.lower()
        reply_to = update.message.reply_to_message
        is_reply_to_bot = reply_to and reply_to.from_user and reply_to.from_user.id == context.bot.id
        if not is_mention and not is_reply_to_bot:
            return
        if is_mention:
            text = re.sub(re.escape(bot_username), "", text, flags=re.IGNORECASE).strip()
        if not text:
            await update.message.reply_text("有什麼事？")
            return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    history = user_histories.setdefault(user_id, [])
    history.append({"role": "user", "content": text})

    try:
        resp = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history[-20:],
            max_tokens=300,
            temperature=0.8,
        )
        reply = re.sub(r"<think>.*?</think>", "", resp.choices[0].message.content, flags=re.DOTALL).strip()
        history.append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("有點問題，等一下再試？")
        print(f"Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.effective_user.first_name or "Friend"
    await update.message.reply_text(f"Hey {name}，我是 oct26th 的 AI 分身。有什麼事？")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_histories.pop(update.effective_user.id, None)
    await update.message.reply_text("對話重置了。")

def main():
    if not TELEGRAM_BOT_TOKEN or not MINIMAX_API_KEY:
        print("❌ 缺少環境變數：TELEGRAM_BOT_TOKEN 或 MINIMAX_API_KEY")
        exit(1)

    print("✓ oct26th bot 啟動中...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✓ Bot running")
    app.run_polling()

if __name__ == "__main__":
    main()
