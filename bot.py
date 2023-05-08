from aiogram import executor
from db import Bot
from dispatcher import dp
import handlers

BotDB = Bot('Accountant.sqlite')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)
