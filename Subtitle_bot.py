import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# импорт токена бота
from token_data import BOT_TOKEN

# для скачивания видео с ютуба
import requests
from urllib.parse import urlencode

# импортируем часть по обработке видео
from VideoToText import recognize_text, extract_audio
from PastSubtOnVideo import add_text_to_video

# импортируем часть по добавлению событий в календарь
from calendar_client import add_event_to_gcal, GoogleCalendar

# объект класса для гугл календаря
obj = GoogleCalendar()

# создаём бота
token = BOT_TOKEN
bot = Bot(token=token)
dp = Dispatcher()


# класс состояний
class Form(StatesGroup):
    google_id = State()
    name = State()
    desc = State()
    start = State()
    end = State()
    Name_google = ""
    Desk_google = ""
    Date_start = ""
    Date_end = ""
    User_id = ""


@dp.message(Command("start"))  # Команда старта
async def start_command(message: types.Message):
    # создание клавиатуры при старте
    kb = [
        [types.KeyboardButton(text="Сделать субтитры"), types.KeyboardButton(text="Добавить задачу в гугл календарь")],
        [types.KeyboardButton(text="Помощь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                         one_time_keyboard=True)
    # здороваемся с пользователем
    await message.answer(
        f"Привет, {message.from_user.full_name}!\nЯ могу создать субтитры к видео или добавить в Google календарь "
        "событие. Все необходимые инструкции появятся при выборе соответствующей функции. Можешь написать Помощь, "
        "если таковая понадобится)",
        reply_markup=keyboard)


@dp.message(Command("help"))  # команда /help
async def help_command(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Сделать субтитры"), types.KeyboardButton(text="Добавить задачу в гугл календарь")],
        [types.KeyboardButton(text="Помощь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                         one_time_keyboard=False)
    await message.answer(
        "Я могу помочь вам сделать субтитры или же добавить задачу в гугл календарь, для подробностей нажмите на одну из этих кнопок.",
        reply_markup=keyboard)


@dp.message(F.text.lower() == "помощь")  # если человек запрашивает помощь через текст или кнопку
async def help_button(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Сделать субтитры"), types.KeyboardButton(text="Добавить задачу в гугл календарь")],
        [types.KeyboardButton(text="Помощь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                         one_time_keyboard=True)
    await message.answer(
        "Я могу помочь вам сделать субтитры или же добавить задачу в гугл календарь, для подробностей нажмите на одну из этих кнопок.",
        reply_markup=keyboard)


@dp.message(F.text.lower() == "сделать субтитры")  # инструкция к загрузке видео
async def subtitles_button(message: types.Message):
    await message.answer(
        "Просто скиньте ссылку на видео с яндекс диска, проверьте что ссылка рабочая и доступна загрузка видео.\n"
        "В случае если происходит ошибка при загрузке видео, попробуйте загрузить его на свой яндекс диск и "
        "поделиться ссылкой.")


@dp.message(F.text.startswith("https://disk.yandex.ru"))  # Если нам кидают ссылку на яндекс диск, то начинаем работу
async def Download_file(message: types.Message):
    video_path = "video.mp4"
    audio_path = "audio.wav"
    output_path = "result.mp4"
    font_size = 30
    # первым делом пытаемся скачать видео, в случае если не получается, сообщаем об этом пользователю
    try:
        base_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download?"
        public_key = message.text
        final_url = base_url + urlencode(dict(public_key=public_key))
        response = requests.get(final_url)
        download_url = response.json()["href"]
        download_response = requests.get(download_url)
        with open(video_path, "wb") as f:
            f.write(download_response.content)
    except:
        await message.answer("что то пошло не так при загрузке файла")
        return 0
    # следующий шаг - извлечение аудиодорожки из видео
    try:
        extract_audio(video_path, audio_path)
    except:
        await message.answer("что то пошло не так при извлечении аудио")
        return 0
    # в следующем шаге извлекаем текст из видео и отправляем текст пользователю
    try:
        recognized_text = recognize_text(audio_path)
        await message.answer(recognized_text)
    except:
        await message.answer("что то пошло не так при распознавании текста")
        return 0
    # затем добавляем текст на видеодорожку и так же отправляем пользователю видеофайл
    try:
        add_text_to_video(video_path, recognized_text, font_size, output_path)
        await message.answer_video(FSInputFile("result.mp4"))
    except:
        await message.answer("что то пошло не так при добавлении субтитров к видео")
        return 0


@dp.message(F.text.lower() == "добавить задачу в гугл календарь")  # инструкция к добавлению события
async def calendar_button(message: types.Message):
    await message.answer("Чтобы добавить событие в календарь Вам нужно предоставить к нему доступ. Выберете в разделе "
                         "«Мои календари» нужный календарь и выберете «Настройки и общий доступ». Найдите раздел "
                         "«Открыть доступ пользователям или группам», добавьте "
                         "lecturebot@lecturebot.iam.gserviceaccount.com доступ на внесение изменений. Пролистайте "
                         "дальше до раздела «Интеграция календаря» (пришлите боту идентификатор календаря).\nКогда "
                         "доступ предоставлен пришлите сообщение !создать событие")


@dp.message(F.text.lower() == "отмена") # на случай, если пользователь передумал создавать событие
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Процесс создания события отменён.")


@dp.message(F.text.lower() == "!создать событие") # начало создания, просим название
async def start_google(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Введите название события.\nДля того чтобы прервать создание события напишите отмена.")


@dp.message(Form.name) # запоминаем название, просим описание
async def process_name(message: types.Message, state: FSMContext):
    await state.set_state(Form.desc)
    Form.Name_google = message.text
    await message.answer("Введите описание события.\nДля того чтобы прервать создание события напишите отмена.")


@dp.message(Form.desc) # запоминаем описание, просим дату начала
async def process_desc(message: types.Message, state: FSMContext):
    await state.set_state(Form.start)
    Form.Desk_google = message.text
    await message.answer("Введите начало события в формате ГГГГ-ММ-ДД.\nДля того чтобы прервать создание события напишите отмена.")


@dp.message(Form.start) # запоминаем дату начала, просим дату окончания
async def process_desc(message: types.Message, state: FSMContext):
    await state.set_state(Form.end)
    Form.Date_start = message.text
    await message.answer("Введите конец события в формате ГГГГ-ММ-ДД (не включительно).\nДля того чтобы прервать создание события напишите отмена.")


@dp.message(Form.end) # запоминаем дату окончания, просим айди
async def process_desc(message: types.Message, state: FSMContext):
    await state.set_state(Form.google_id)
    Form.Date_end = message.text
    await message.answer("Введите свой айди пользователя.\nДля того чтобы прервать создание события напишите отмена.")


@dp.message(Form.google_id) # получаем айди, создаём событие
async def process_desc(message: types.Message, state: FSMContext):
    await state.clear()
    Form.User_id = message.text
    try:
        add_event_to_gcal(title=Form.Name_google, desc=Form.Desk_google, calendarid=Form.User_id, start=Form.Date_start,
                          end=Form.Date_end)
        await message.answer("Событие успешно создано")
    except:
        await message.answer("Произошла непредвиденная ошибка, проверьте введённые данные")


@dp.message() # в остальных случаях отсылаем на помощь
async def send_help(message: types.Message):
    await message.answer("Напишите Помощь для получения списка команд")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
