from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from logging import basicConfig, INFO
from config import token 
import os, sqlite3, time, uuid

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)

connection = sqlite3.connect('client.db')
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INT,
    first_name VARCHAR(200), 
    last_name VARCHAR(200), 
    username VARCHAR(200), 
    created VARCHAR(200)
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS payment(
    payment_code INT,
    first_name VARCHAR(200), 
    last_name VARCHAR(200),
    direction VARCHAR(100),
    month VARCHAR(100),
    amount VARCHAR(20),
    date VARCHAR(100)
);
""")

paymant_keyboard = [
    types.InlineKeyboardButton("Оплата", callback_data='paymant_but')

]
paymant_button = types.InlineKeyboardMarkup().add(*paymant_keyboard)



@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    exists_user = cursor.fetchall()
    if not exists_user:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?);",
                       (message.from_user.id, message.from_user.first_name,
                        message.from_user.last_name, message.from_user.username, time.ctime()))
        cursor.connection.commit()
    await message.answer(f"Здравствуйте {message.from_user.full_name}")
    await message.answer("Если вы сделали оплату, нажмите на кнопку", reply_markup=paymant_button)

class PaymentState(StatesGroup):
    first_name = State()
    last_name = State()
    direction = State()
    month = State()
    amount = State()

@dp.callback_query_handler(lambda call: call.data == "paymant_but")
async def payment_student(message:types.Message):
    await bot.send_message(message.message.chat.id,"Для оплаты заполните следующие поля: (имя, фамилия, направление, месяц, сумма)")
    await bot.send_message(message.message.chat.id,"Теперь напишите свое имя:")
    await PaymentState.first_name.set()

@dp.message_handler(state=PaymentState.first_name)
async def get_last_name(message:types.Message, state:FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Отлично, теперь вашу фамилию:")
    await PaymentState.last_name.set()

@dp.message_handler(state=PaymentState.last_name)
async def get_direction(message:types.Message, state:FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("В каком направлении вы учитесь?")
    await PaymentState.direction.set()

@dp.message_handler(state=PaymentState.direction)
async def get_month(message:types.Message, state:FSMContext):
    await state.update_data(direction=message.text)
    await message.answer("Какой месяц обучения вы оплатили?")
    await PaymentState.month.set()

@dp.message_handler(state=PaymentState.month)
async def get_amount(message:types.Message, state:FSMContext):
    await state.update_data(month=message.text)
    await message.answer("Сколько вы оплатили?")
    await PaymentState.amount.set()

@dp.message_handler(state=PaymentState.amount)
async def generate_payment(message:types.Message, state:FSMContext):
    await state.update_data(amount=message.text)
    result = await storage.get_data(user=message.from_user.id)
    print(result)
    generate_payment_code = int(str(uuid.uuid4().int)[:10])
    print(generate_payment_code)
    cursor.execute("INSERT INTO payment VALUES (?, ?, ?, ?, ?, ?, ?);",
                    (generate_payment_code, result['first_name'], result['last_name'],
                     result['direction'], result['month'], result['amount'], time.ctime()))
    cursor.connection.commit()
    payment_text = f"""Оплата курса {result['direction']}
Имя: {result['first_name']}
Фамилия: {result['last_name']}
Направление: {result['direction']}
Месяц: {result['month']}
Количество: {result['amount']}
Код оплаты: {generate_payment_code}
Время: {time.ctime()}"""
    await message.answer(payment_text)
    await bot.send_message(-4070763776, payment_text)
    await state.finish()

executor.start_polling(dp, skip_updates=True)