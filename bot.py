# bot.py

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from config import API_TOKEN
from movie_api import get_movie_recommendation, genre_map

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    buttons = [
        [InlineKeyboardButton(text=genre.title(), callback_data=genre)]
        for genre in genre_map
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("🎞 Choose your favorite genre:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data in genre_map)
async def process_genre(callback: types.CallbackQuery):
    genre = callback.data
    text, poster_url = get_movie_recommendation(genre)
    await bot.answer_callback_query(callback.id)

    if poster_url:
        await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=poster_url,
            caption=text,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await bot.send_message(callback.from_user.id, text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
