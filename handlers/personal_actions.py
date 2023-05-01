from aiogram import types
from bot import BotDB
import config
from consts import Banks
from dispatcher import dp, bot
import re


@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add(message.from_user.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/history")
    btn2 = types.KeyboardButton("/statistics")
    btn3 = types.KeyboardButton("/help")
    markup.add(btn1, btn2, btn3)

    await message.bot.send_message(message.from_user.id, text = "Добро пожаловать! Готов помочь Вам с бюджетом.", reply_markup=markup)


@dp.message_handler(commands = ("earned", "e"), commands_prefix = "/!")
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/history")
    btn2 = types.KeyboardButton("/statistics")
    btn3 = types.KeyboardButton("/help")
    markup.add(btn1, btn2, btn3)

    vars = (('/spent', '/s', '!spent', '!s'), ('/earned', '/e', '!earned', '!e'))
    oper = '-' if message.text.startswith(vars[0]) else '+'

    value = message.text
    for i in vars:
        for j in i:
            value = value.replace(j, '').strip()

    if len(value) > 0:
        helper = re.findall(r"\d+(?:.\d+)?", value)
        if len(helper) > 0:
            value = float(helper[0].replace(',', '.'))

            BotDB.add_record(message.from_user.id, oper, value)

            if oper == '-':
                await message.reply(text="✅ Запись о <u><b>расходе</b></u> была внесена успешно!", reply_markup=markup)
            else:
                await message.reply(text="✅ Запись о <u><b>доходе</b></u> была внесена успешно!", reply_markup=markup)
        else:
            await message.reply(text="Не удалось распознать сумму!", reply_markup=markup)
    else:
        await message.reply(text="Сумма не введена!", reply_markup=markup)


@dp.message_handler(commands = ("spent", "s"), commands_prefix = "/!")
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/history")
    btn2 = types.KeyboardButton("/statistics")
    btn3 = types.KeyboardButton("/help")
    markup.add(btn1, btn2, btn3)

    vars = (('/spent', '/s', '!spent', '!s'), ('/earned', '/e', '!earned', '!e'))
    oper = '-' if message.text.startswith(vars[0]) else '+'

    value = message.text
    for i in vars:
        for j in i:
            value = value.replace(j, '').strip()
            arr = value.split()

    if len(arr) > 0 and len(arr[0]) > 0:
        helper = re.findall(r"\d+(?:.\d+)?", arr[0])
        if len(helper) > 0:
            num = float(helper[0].replace(',', '.'))

            BotDB.add_record(message.from_user.id, oper, num, arr[1])

            if oper == '-':
                await message.reply(text="✅ Запись о <u><b>расходе</b></u> была внесена успешно!", reply_markup=markup)
            else:
                await message.reply(text="✅ Запись о <u><b>доходе</b></u> была внесена успешно!", reply_markup=markup)
        else:
            await message.reply(text="Не удалось распознать сумму!", reply_markup=markup)
    else:
        await message.reply(text="Сумма не введена!", reply_markup=markup)


@dp.message_handler(commands = ("history", "h"), commands_prefix = "/!")
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/history")
    btn2 = types.KeyboardButton("/statistics")
    btn3 = types.KeyboardButton("/help")
    markup.add(btn1, btn2, btn3)

    vars = ('/history', '/h', '!history', '!h')
    time_dict = {
        "day": ('today', 'day', 'сегодня', 'день'),
        "month": ('month', 'месяц'),
        "year": ('year', 'год'),
    }

    cmd = message.text
    for r in vars:
        cmd = cmd.replace(r, '').strip()

    time = 'day'
    if len(cmd) > 0:
        for k in time_dict:
            for als in time_dict[k]:
                if als == cmd:
                    time = k

    records = BotDB.get_records(message.from_user.id, time)

    if len(records) > 0:
        answer = f"🕘 История операций за {time_dict[time][-1]}\n\n"

        for r in records:
            answer += "<b>" + ("➖ Расход" if not r[2] else "➕ Доход") + "</b>"
            answer += f" - {abs(r[3])}"
            answer += f" <i>({r[5][:11] + str(int(r[5][11:13]) + 3) + r[5][13:]}) {'➡' if r[3] < 0 else ''}  {r[4].capitalize()}</i>\n"

        answer += "<b>" + " Итого на счёте: " + "</b>"
        answer += f"{BotDB.total(message.from_user.id)[0][0]}"

        await message.reply(text=answer, reply_markup=markup)
    else:
        await message.reply(text="Записей не обнаружено!", reply_markup=markup)


@dp.message_handler(commands = ("statistics", "stat"), commands_prefix = "/!")
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/history")
    btn2 = types.KeyboardButton("/statistics")
    btn3 = types.KeyboardButton("/help")
    markup.add(btn1, btn2, btn3)

    helper = BotDB.get_stat(message.from_user.id)
    answer = ''
    i = 1

    for elem in helper:
        answer += "<b>" + f"{i}. {elem[0].capitalize()}" + "</b>" + ' ▶ ' + f"{abs(elem[1])}\n"
        i += 1

    if answer != '':
        await message.reply(text=answer, reply_markup=markup)


@dp.message_handler(commands = ("help"), commands_prefix = "/!")
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/history")
    btn2 = types.KeyboardButton("/statistics")
    btn3 = types.KeyboardButton("/help")
    markup.add(btn1, btn2, btn3)

    answer = 'Список допустимых команд:\n'
    answer += "<b>" + "/start" + "</b>" + " - Начало общения с ботом\n"
    answer += "<b>" + "/earned" + "</b>" + " - Добавление записи о доходе\n"
    answer += "<b>" + "/spent" + "</b>" + " - Добавление записи о расходе (сумма и категория пишутся через пробел)\n"
    answer += "<b>" + "/history" + "</b>" + " - История опраций (срок пишется через пробел)\n"
    answer += "<b>" + "/statistics" + "</b>" + " - Убываущий рейтинг затрат\n"

    await message.reply(text=answer, reply_markup=markup)


@dp.message_handler(content_types = ['location'])
async def start(message):
    lon = message.location.longitude
    lat = message.location.latitude

    distances = []

    for elem in Banks:
        result = (lon - elem["lon"])**2 + (lat - elem["lat"])**2
        distances.append(result)

    ind = distances.index(min(distances))

    await bot.send_message(message.chat.id, "Ближайший к Вам Сбербанк из нашего списка")
    await bot.send_venue(message.chat.id, Banks[ind]["lat"], Banks[ind]["lon"], Banks[ind]["title"], Banks[ind]["add"])
