import os
import re
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен берём из переменных окружения (так безопаснее)
BOT_TOKEN = os.environ.get("9043338967:AAHHvVYN7LgMI3uls2q7h4ugHe8kE9mI7YI")
# Ваш юзернейм тоже можно вынести в переменную, но пока оставим так
YOUR_USERNAME = "Hddddtt"  # Замените на свой

bot = telebot.TeleBot(BOT_TOKEN)
PRICE_PATTERN = re.compile(r"^/price\s+(\S+)\s+(\d+)\s+stars$", re.IGNORECASE)

@bot.message_handler(commands=['myid'])
def get_my_id(message):
    bot.reply_to(message, f"Твой ID: `{message.from_user.id}`", parse_mode="Markdown")

@bot.message_handler(commands=['price'])
def handle_price_command(message):
    match = PRICE_PATTERN.match(message.text.strip())
    if not match:
        bot.reply_to(message, "❌ Формат: `/price <ссылка> <цена> stars`", parse_mode="Markdown")
        return
    
    nft_link, price = match.group(1), match.group(2)
    caption = f"🎁 *Предложение NFT*\n\n🔗 {nft_link}\n💰 *{price} Stars*\n\nНажмите кнопку ниже."
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🎁 Передать NFT", callback_data="request_gift"))
    bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "request_gift")
def handle_gift_button(call):
    bot.answer_callback_query(call.id, "Переходим в профиль...")
    new_text = (
        f"✅ *Запрос отправлен!*\n\n"
        f"Перейдите в профиль отправителя и нажмите «Отправить подарок»:\n"
        f"👉 [Перейти в профиль](https://t.me/{YOUR_USERNAME})"
    )
    bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id, 
                          parse_mode="Markdown", reply_markup=None)

if __name__ == "__main__":
    bot.polling(none_stop=True)
