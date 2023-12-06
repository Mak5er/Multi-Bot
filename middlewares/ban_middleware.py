from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler  # отменяет вызов хэндлера
from aiogram.dispatcher.middlewares import BaseMiddleware  # класс Middleware от Aiogram
from aiogram.types import Message, CallbackQuery, InlineQuery

from services import DataBase

db = DataBase()


class UserBannedMiddleware(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        try:
            user = await db.status(message.from_user.id)
        except:
            user = 'user'
        if user == 'ban':
            if message.chat.type == 'private':
                await message.answer(
                '*You are banned please contact to @mak5er for more information!*', parse_mode="Markdown"
            )
            raise CancelHandler

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        user = await db.status(call.from_user.id)
        if user == 'ban':
            await call.answer(
                'You are banned please contact to @mak5er for more information!',
                show_alert=True
            )
            raise CancelHandler

    async def on_process_inline_query(self, query: InlineQuery, data: dict):
        user = await db.status(query.from_user.id)
        if user == 'ban':
            raise CancelHandler


def setup_ban_middleware(dp: Dispatcher):
    dp.middleware.setup(UserBannedMiddleware())


def setup_ban_middlewares(dp: Dispatcher):
    setup_ban_middleware(dp)
