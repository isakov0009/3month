from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3, logging
from config import token


bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)



class AddTask(StatesGroup):
    title = State()
    time = State()

start_buttons = [
    types.KeyboardButton('/addtask'),
    types.KeyboardButton('/list'),
    types.KeyboardButton('/delete'),
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)




@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я бот для управления делами. Чтобы добавить дело, используй команду /addtask.", reply_markup=start_keyboard)



@dp.message_handler(commands=['addtask'])
async def cmd_addtask(message: types.Message):
    await AddTask.title.set()
    await message.reply("Введите название дела:")



@dp.message_handler(state=AddTask.title)
async def process_task_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await AddTask.next()
    await message.reply("Введите время выполнения дела (в формате ЧЧ:ММ):")



@dp.message_handler(state=AddTask.time)
async def process_task_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text

    save_task(data['title'], data['time'])

    await state.finish()
    await message.reply("Дело успешно добавлено!")


@dp.message_handler(commands=['list'])
async def cmd_list(message: types.Message):
    tasks = get_tasks()
    if tasks:
        tasks_text = '\n'.join(tasks)
        await message.reply(f"Список дел:\n{tasks_text}")
    else:
        await message.reply("Список дел пуст.")


@dp.message_handler(commands=['delete'])
async def cmd_delete(message: types.Message):
    tasks = get_tasks()
    if tasks:
        keyboard_markup = InlineKeyboardMarkup()
        for task in tasks:
            button = InlineKeyboardButton(task, callback_data=task)
            keyboard_markup.add(button)

        await message.reply("Выберите дело для удаления:", reply_markup=keyboard_markup)
    else:
        await message.reply("Список дел пуст.")



@dp.callback_query_handler(lambda callback_query: True)
async def process_delete_task(callback_query: types.CallbackQuery):
    task = callback_query.data
    delete_task(task)
    await bot.send_message(callback_query.from_user.id, f"Дело '{task}' удалено.")


def create_table():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_task(title, time):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, time) VALUES (?, ?)', (title, time))
    conn.commit()
    conn.close()


def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return [task[0] for task in tasks]


def delete_task(task):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE title=?', (task,))
    conn.commit()
    conn.close()


create_table()

executor.start_polling(dp,skip_updates=True)