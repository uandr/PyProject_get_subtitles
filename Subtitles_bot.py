import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

token = BOT_TOKEN
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Сделать субтитры"), types.KeyboardButton(text="Добавить задачу в гугл календарь")],
        [types.KeyboardButton(text="Помощь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                         one_time_keyboard=False)  # когда реализуются функции, сделать True
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=keyboard)


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("напишите Помощь")


@dp.message(F.text.lower() == "помощь")
async def help_button(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Сделать субтитры"), types.KeyboardButton(text="Добавить задачу в гугл календарь")],
        [types.KeyboardButton(text="Помощь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                         one_time_keyboard=False)  # когда реализуются функции, сделать True
    await message.answer("Ну допустим я помог", reply_markup=keyboard)


@dp.message(F.text.lower() == "сделать субтитры")
async def subtitles_button(message: types.Message):
    await message.answer("субтитры в разработке")


@dp.message(F.text.lower() == "добавить задачу в гугл календарь")
async def calendar_button(message: types.Message):
    await message.answer("не поверите, но это тоже пока в разработке")


@dp.message()
async def send_help(message: types.Message):
    await message.answer("Напишите Помощь для получения списка команд")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
