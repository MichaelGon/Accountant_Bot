from aiogram import Bot, Dispatcher
from config import TOKEN
from filters import OwnerFilter, AdminFilter, MemberCanRestrictFilter
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

dp.filters_factory.bind(OwnerFilter)
dp.filters_factory.bind(AdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)
