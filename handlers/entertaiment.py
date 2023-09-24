import asyncio

from aiogram import types

from keyboards import keyboards as kb
from main import dp, _, bot
from middlewares.throttling_middleware import rate_limit


@rate_limit(1)
@dp.message_handler(text=['🎮Entertainments', '🎮Розваги'])
async def entertainments_handler(message: types.Message):
    await message.answer(_('Hi, this is the entertainment section!'), reply_markup=kb.return_entertainment_keyboard())


@rate_limit(4)
@dp.message_handler(
    text=["Боулінг🎳", "Дартс🎯", "Кубик🎲", "Баскетбол🏀", "Казино🎰", "Футбол⚽", 'Bowling🎳', 'Darts🎯', 'Dice🎲',
          'Basketball🏀', 'Casino🎰', 'Football⚽'])
async def entertainment(message: types.Message):
    result: types.Message = await bot.send_dice(message.chat.id, emoji=f'{message.text}',
                                                allow_sending_without_reply=True)
    dice_result = result.dice.value

    await asyncio.sleep(4)

    if message.text in ['Basketball🏀', "Баскетбол🏀"]:
        if dice_result in [5, 4]:
            await message.reply(text=_("Yay, I scored!"))
        elif dice_result == 3:
            await message.reply(text=_("Uhm..."))
        else:
            await message.reply(text=_("I missed :("))

    elif message.text in ['Football⚽', "Футбол⚽"]:
        if dice_result in [5, 4, 3]:
            await message.reply(text=_("Yay, I scored!"))
        else:
            await message.reply(text=_("I missed :("))

    elif message.text in ['Bowling🎳', "Боулінг🎳"]:
        if dice_result == 1:
            await message.reply(text=_("I missed :("))
        elif dice_result == 6:
            await message.reply(text=_("Yay, I scored a strike!"))
        elif dice_result == 2:
            dice_result = dice_result - 1
            await message.reply(
                text=_("I knocked down a *{dice_result}* bowling pin.").format(dice_result=dice_result),
                parse_mode='Markdown')
        else:
            await message.reply(
                text=_("I knocked down a *{dice_result}* bowling pin.").format(dice_result=dice_result),
                parse_mode='Markdown')

    elif message.text in ['Casino🎰', "Казино🎰"]:
        if dice_result in [1, 64, 22, 43]:
            await message.reply(_("Yay, I win!"))
        elif dice_result in [16, 32, 48]:
            await message.reply(_('Almost... :('))
        else:
            await message.reply(_("I lost :("))

    elif message.text in ['Darts🎯', "Дартс🎯"]:
        if dice_result == 6:
            await message.reply(_("Into the apple!"))
        elif dice_result == 1:
            await message.reply(_("I missed :("))
        else:
            line = dice_result - 1
            await message.reply(_("I'm on the *{line}* line").format(line=line), parse_mode='Markdown')

    elif message.text in ['Dice🎲', 'Кубик🎲']:
        await message.reply(_("The dice rolled *{dice_result}*").format(dice_result=dice_result),
                            parse_mode='Markdown')
