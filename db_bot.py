from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from logging import basicConfig, INFO
from config import token 
import sqlite3, time

bot = Bot(token=token)
storage = MemoryStorage()
dq = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)
 
connection = sqlite3.connect('users.db')
cursor = connection.cursor ()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    created VARCHAR(50)
               
    );
    """)

cursor.connection.commit()

@dq.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    result = cursor.fetchall()
    print(result)
    if result == []:
        cursor.execute(f"INSERT INTO  users VALUES (?,?,?,?,?)", (
        message.from_user.id, message.from_user.username,
        message.from_user.first_name, message.from_user.last_name,
        time.ctime()
        ))
        cursor.connection.commit()
    await message.answer(f"Здравствуйте {message.from_user.first_name}")

class MailingState(StatesGroup):
    message = State()

@dq.message_handler(commands='mailing')
async def get_text_mailing(message:types.Message):
    await message.answer("Отправьте свой текст для рассылки")
    await MailingState.message.set()

@dq.message_handler(state=MailingState.message)
async def mailing_users(message:types.Message, state:FSMContext):
    await message.answer("Начинаю рассылку...")
    cursor.execute("SELECT id FROM users;")
    users_id = cursor.fetchall()
    print(users_id)
    for user_id in users_id:
        await bot.send_message(user_id[0], message.text)
    await state.finish()



executor.start_polling(dq)