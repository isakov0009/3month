from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
from config import token 
import requests, os 

bot = Bot(token=token)
dp =Dispatcher(bot)
basicConfig(level=INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}")

@dp.message_handler()
async def download_send_video(message:types.Message):
    if 'tiktok.com' in message.text:
        await message.answer("Начинаю скачивать видео...")
        split_url = message.text.split('/')
        current_id = split_url[5].split('?')[0]
        video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()
        video_url = video_api.get('aweme_list')[0].get('video').get('play_addr').get('url_list')[0]
        if video_url:
            video_id = video_api.get('aweme_list')[0].get('aweme_id')
            try:
                os.mkdir('video')
            except:
                pass
            try:
                with open(f'video/{video_id}.mp4', 'wb') as video_file:
                    video_file.write(requests.get(video_url).content)
                await message.answer(f"Видео {video_id} успешно скачан")
                with open(f'video/{video_id}.mp4', 'rb') as read_video_file:
                    await message.answer_video(read_video_file)
            except Exception as error:
                await message.answer(f"Ошибка: {error}")
    else:
        await message.answer("Неверная ссылка на видео")

executor.start_polling(dp)
