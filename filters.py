from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from config import TOKEN


class OwnerFilter(BoundFilter):
    key = "is_owner"

    def __init__(self, is_owner):
        self.is_owner = is_owner

    async def check(self, message: types.Message):
        return message.from_user.id == TOKEN


class AdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        mem = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return mem.is_chat_admin() == self.is_admin


class MemberCanRestrictFilter(BoundFilter):
    key = 'member_can_restrict'

    def __init__(self, member_can_restrict: bool):
        self.member_can_restrict = member_can_restrict

    async def check(self, message: types.Message):
        mem = await message.bot.get_chat_member(message.chat.id, message.from_user.id)

        return (mem.is_chat_creator() or mem.can_restrict_members) == self.member_can_restrict
