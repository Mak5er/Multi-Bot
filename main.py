from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config
from middlewares import setup_middleware

bot = Bot(token=config.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

i18n = setup_middleware(dp)

_ = i18n.gettext

if __name__ == '__main__':
    from handlers.users import dp

    from handlers.qr_code import dp

    from handlers.weather import dp

    from handlers.random_gen import dp

    from handlers.tasks import dp

    import keep_alive

    keep_alive.keep_alive()
    executor.start_polling(dp, skip_updates=True)
