import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Берем токен из настроек BotHost (ничего вписывать сюда не надо)
BOT_TOKEN = os.environ.get("9043338967:AAHHvVYN7LgMI3uls2q7h4ugHe8kE9mI7YI")

# ВПИШИ СЮДА СВОЙ ЮЗЕРНЕЙМ БЕЗ @ (например: "IvanIvanov")
YOUR_USERNAME = "Hddddtt" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для офферов.\n"
        "Отправь мне: /price <ссылка> <цена> stars\n"
        "Пример: /price https://t.me/nft/InstantRamen-170965 1000 stars"
    )

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    # Ищем команду в формате: /price ссылка цифра stars
    match = re.match(r"^/price\s+(\S+)\s+(\d+)\s+stars$", text, re.IGNORECASE)
    
    if not match:
        await update.message.reply_text("❌ Ошибка формата. Напиши так:\n/price https://t.me/nft/... 1000 stars")
        return

    nft_link = match.group(1)
    price = match.group(2)

    caption = (
        f"🎁 *Предложение NFT*\n\n"
        f"🔗 Ссылка: {nft_link}\n"
        f"💰 Цена: *{price} Stars*\n\n"
        f"Жми кнопку ниже, чтобы запросить подарок."
    )

    keyboard = [[InlineKeyboardButton("🎁 Передать NFT", callback_data="request_gift")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(caption, parse_mode="Markdown", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Убираем "часики" загрузки

    if query.data == "request_gift":
        # Меняем текст сообщения и убираем кнопку
        new_text = (
            f"✅ *Запрос отправлен!*\n\n"
            f"Перейди в профиль отправителя и нажми «Отправить подарок»:\n"
            f"👉 [Перейти в профиль](https://t.me/{Hddddtt)"
        )
        await query.edit_message_text(text=new_text, parse_mode="Markdown", disable_web_page_preview=True)

def main():
    if not BOT_TOKEN:
        print("❌ Токен не найден! Проверь переменные на BotHost.")
        return

    # Запускаем приложение
    app = Application.builder().token(BOT_TOKEN).build()

    # Добавляем команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
