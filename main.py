# from aiogram import Bot,Dispatcher,types,executor
# from config import token
# from config import random

# bot = Bot(token = token)
# dp = Dispatcher(bot)

# @dp.message_handler(commands=["start"])
# async def start(message:types.Message):
#     await message.answer (f"Здрастуете" {message.from_user.full_name} \nВас приветствует Random Bot нажмите /Go что бы сыграть с мной игру")
# from logging import basicConfig, INFO
# from config import token 

# bot = Bot (token= token)
# dp = Dispatcher(bot   aiogram import Bot, Dispatcher, types, executor)   



# @dp.message_handler(commands=['Go'])
# async def azino777(message:types.Message):
#     await message.answer("Я загадал число от 1 до 3 угадайте")

# @dp.message_handler(text= [1,2,3])
# async def azino(message:types.Message):
#     azi= random.randint(1,3)
#     answer = int(message.text)
    
#     if answer == azi:
#         await message.reply(f"Вы угадали {azi}")
#         await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
        
#     else:
#         await message.answer ("Вы не угадали")
#         await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')
#         await message.answer(f"правильное число: {azi}" )


# executor.start_polling(dp)
