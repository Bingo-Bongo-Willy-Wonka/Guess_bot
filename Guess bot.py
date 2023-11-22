from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

import json
import os
from dotenv import load_dotenv

import random


load_dotenv()
TOKEN = os.getenv('TOKEN')

MY_ID = os.getenv('MY_ID')

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


# users = {123:
#     {
#     "in_game": False,
#     "attempts": None,
#     "secret_number": None,
#     "wins": 0,
#     "games": 0
#     }
#          }


new_user = {"in_game": False,
    "attempts": None,
    "secret_number": None,
    "wins": 0,
    "games": 0}

ATTEMPTS = 6

file_r = open("guess_bot_data.json", "r")
users = json.load(file_r)
file_r.close()


def return_random_number():
    return random.randint(0, 100)


async def start_command(mess: Message):

    if str(mess.from_user.id) in list(users.keys()):
        await mess.answer("1Я бот угадайка. Сыграем в игру?")
    else:
        users[str(mess.from_user.id)] = new_user
        await mess.answer("Я бот угадайка. Сыграем в игру?")
        print(users)
    await saving()

async def help_command(mess: Message):
    await mess.answer("Правила игры:"
                      "\nЯ загадываю число от 0 до 100."
                      f"\nУ тебя есть {ATTEMPTS} попыток чтобы угадать."
                      f"\nОтмена игры считается за проигрыш."
                      f"\nСыграем?"
                      f"\n\nСписок команд:"
                      f"\n/cancel - отменить игру."
                      f"\n/stat - статистика.")


async def start_game(mess: Message):
    if not users[str(mess.from_user.id)]['in_game']:
        users[str(mess.from_user.id)]['in_game'] = True
        users[str(mess.from_user.id)]['attempts'] = ATTEMPTS
        users[str(mess.from_user.id)]['secret_number'] = return_random_number()
        await mess.answer('Я загадал число. Попробуй угадать!')
    else:
        await mess.answer(f'Мы уже играем. У вас {users[str(mess.from_user.id)]["attempts"]} попыток')


async def cancel_game(mess: Message):
    if users[str(mess.from_user.id)]['in_game']:
        users[str(mess.from_user.id)]['in_game'] = False
        users[str(mess.from_user.id)]['attempts'] = None
        users[str(mess.from_user.id)]['secret_number'] = None
        users[str(mess.from_user.id)]['games'] += 1
        await mess.answer('Игра отменена')
    else:
        await mess.answer('А мы и не играем.')


async def deny_game(mess: Message):
    if not users[str(mess.from_user.id)]['in_game']:
        await mess.answer('Жаль. Напиши если захочешь.')
    else:
        users[str(mess.from_user.id)]['in_game'] = False
        users[str(mess.from_user.id)]['attempts'] = None
        users[str(mess.from_user.id)]['secret_number'] = None
        users[str(mess.from_user.id)]['games'] += 1
        await mess.answer('Игра отменена')


async def attempt_message(mess: Message):
    if users[str(mess.from_user.id)]['in_game']:
        users[str(mess.from_user.id)]['attempts'] -= 1
        if int(mess.text) == users[str(mess.from_user.id)]['secret_number']:
            users[str(mess.from_user.id)]['in_game'] = False
            users[str(mess.from_user.id)]['attempts'] = None
            users[str(mess.from_user.id)]['secret_number'] = None
            users[str(mess.from_user.id)]['games'] += 1
            users[str(mess.from_user.id)]['wins'] += 1
            await bot.send_message(chat_id=MY_ID, text=str(users[str(mess.from_user.id)]) + '\n' + str(mess.from_user.first_name))
            await mess.answer('Ты угадал число! Сыграем снова?')

        elif int(mess.text) < users[str(mess.from_user.id)]['secret_number']:
            await mess.answer('Мое число больше')
        elif int(mess.text) > users[str(mess.from_user.id)]['secret_number']:
            await mess.answer('Мое число меньше')

        if users[str(mess.from_user.id)]['attempts'] == 0:
            users[str(mess.from_user.id)]['in_game'] = False
            users[str(mess.from_user.id)]['attempts'] = None
            users[str(mess.from_user.id)]['secret_number'] = None
            users[str(mess.from_user.id)]['games'] += 1
            await mess.answer('У тебя не осталось попыток. Сыграем снова?')
            await bot.send_message(chat_id=MY_ID, text=str(users[str(mess.from_user.id)])+'\n'+str(mess.from_user.first_name))
    else:
        await mess.answer('Мы не играем. Хочешь сыграть?')


# async def attempt_message(mess: Message):
#     if user['in_game'] and user['attempts'] > 1:
#         user['attempts'] -= 1
#
#         if int(mess.text) > user['secret_number']:
#             await mess.answer('Мое число меньше')
#
#         if int(mess.text) < user['secret_number']:
#             await mess.answer('Мое число больше')
#
#         if int(mess.text) == user['secret_number']:
#             user['in_game'] = False
#             user['attempts'] = None
#             user['secret_number'] = None
#             user['games'] += 1
#             user['wins'] += 1
#             await bot.send_message(chat_id=612635111, text=str(user)+'\n'+str(mess.from_user.first_name))
#             await mess.answer('Ты угадал число! Сыграем снова?')
#
#     elif user['in_game'] and user['attempts'] == 1:
#         if int(mess.text) == user['secret_number']:
#             user['in_game'] = False
#             user['attempts'] = None
#             user['secret_number'] = None
#             user['games'] += 1
#             user['wins'] += 1
#             await mess.answer('Ты угадал число! Сыграем снова?')
#             await bot.send_message(chat_id=612635111, text=str(user)+'\n'+str(mess.from_user.first_name))
#         else:
#             user['in_game'] = False
#             user['attempts'] = None
#             user['secret_number'] = None
#             user['games'] += 1
#             await mess.answer('У тебя не осталось попыток. Сыграем снова?')
#             await bot.send_message(chat_id=612635111, text=str(user)+'\n'+str(mess.from_user.first_name))
#     elif user['in_game'] and user['attempts'] == 0:
#         user['in_game'] = False
#         user['attempts'] = None
#         user['secret_number'] = None
#         user['games'] += 1
#         await mess.answer('У тебя не осталось попыток. Сыграем снова?')
#         await bot.send_message(chat_id=612635111, text=str(user) + '\n' + str(mess.from_user.first_name))
#     else:
#         await mess.answer('Мы не играем. Хочешь сыграть?')


async def stat_command(mess: Message):

    mesto: int
    vsego: int = len(users)
    users_rate = (str(mess.from_user.id), users[str(mess.from_user.id)]['wins'])
    table = []
    for key, value in users.items():
        table.append((key, value['wins']))

    sorted_table = sorted(table, key=lambda x: x[1], reverse=True)
    print(sorted_table)
    print("твое место:", sorted_table.index(users_rate) + 1)

    mesto = sorted_table.index(users_rate) + 1
    await mess.answer(f'Кол-во игр: {users[str(mess.from_user.id)]["games"]}'
                      f'\nКол-во побед: {users[str(mess.from_user.id)]["wins"]}'
                      f'\nМесто в рейтинге: {mesto} из {vsego} ')



async def other_messages(mess: Message):
    if users[str(mess.from_user.id)]['in_game']:
        await mess.answer('Пока мы играем в игру я воспринимаю только числа')
    else:
        await mess.answer('Я не понимаю.\n/help - правила игры и список команд')


async def saving():
    while True:
        file_w = open("guess_bot_data.json", "w")
        json.dump(users, file_w)
        print("сохранено")
        file_w.close()
        await asyncio.sleep(10)


async def rating(mess: Message):
    mesto: int
    vsego: int = len(users)
    users_rate = (str(mess.from_user.id), users[str(mess.from_user.id)]['wins'])
    table = []
    for key, value in users.items():
        table.append((key, value['wins']))

    sorted_table=sorted(table, key= lambda x: x[1], reverse=True)
    print(sorted_table)
    print("твое место:", sorted_table.index(users_rate)+1)

    mesto = sorted_table.index(users_rate)+1


    await mess.answer(f"Твое место: {mesto} из {vsego}")








dp.message.register(start_command, Command(commands='start'))
dp.message.register(help_command, Command(commands='help'))
dp.message.register(cancel_game, Command(commands='cancel'))
dp.message.register(start_game, F.text.lower().in_(['да', 'давай', 'давай сыграем', 'играть', 'сыграем', 'хочу играть']))
dp.message.register(deny_game, F.text.lower().in_(['не', 'нет', 'не хочу', 'не сейчас', 'не хочу играть']))
dp.message.register(attempt_message, lambda x: x.text and x.text.isdigit())
dp.message.register(stat_command, Command(commands='stat'))
dp.message.register(rating, Command(commands='rating'))
dp.message.register(other_messages)




dp.run_polling(bot)

