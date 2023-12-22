from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
from config import token 

bot = Bot (token= token)
dp = Dispatcher(bot)
basicConfig(level=INFO)

start_buttons = [
    types.KeyboardButton("0 нас"),
    types.KeyboardButton("Курсы"),
    types.KeyboardButton("Адрес"),
    types.KeyboardButton("Контакты"),
    types.KeyboardButton("Записаться", request_contact=True)
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)




@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}", reply_markup=start_keyboard)

@dp.message_handler(text="0 нас")
async def about_us(message:types.Message):
    await message.reply("Geeks - ето айти курсы в Бишкеке, Кара-Балта и Оше оснаванная в 2019 году")

@dp.message_handler(text="Адрес")
async def address(message:types.Message):
    await message.answer("Наш адрес: город Ош, мырзалы Аматова 1Б (БЦ Томирис)")
    await message.answer_location(40.51932802044946, 72.8030024754967)

@dp.message_handler(text="Контакты") 
async def send_contacts(message:types.Message):
    await message.answer("Вот контакты наших менеджеров:")
    await message.answer_contact("+996777888111", "tariel", "isakov")
    await message.answer_contact("+996111222333", "erbol", "Abdyldabekov")

courses_buttons = [
    types.KeyboardButton("Beckend"),
    types.KeyboardButton("Frontend"),  
    types.KeyboardButton("ios"), 
    types.KeyboardButton("Andoid"),  
    types.KeyboardButton("UX/UI"),
    types.KeyboardButton("Детское программирование"),
    types.KeyboardButton("Основы программирование"),
    types.KeyboardButton("Назад")
]
courses_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_buttons)

@dp.message_handler(text="Курсы")
async def get_courses(message:types.Message):
    await message.answer("Вот список наших курсов", reply_markup=courses_keyboard)


@dp.message_handler(text="Backend")
async def backend(message:types.Message):
    await message.answer("Backend - это внутренная сторона сайта или приложения которую не видно обычному пользователю")


@dp.message_handler(text="Frontend")
async def frontend(message:types.Message):
    await message.answer("Frontend - это лицевая стороная сайта или приложения где пользователь может видеть")



@dp.message_handler(text="Назад")
async def bact_start(message:types.Message):
    await start(message)

executor.start_polling(dp)