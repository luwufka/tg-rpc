import os
from aiogram import Bot, Dispatcher
from aiogram.types import BufferedInputFile, Message, InputMediaPhoto
from aiogram.enums import ParseMode
from loguru import logger
from colorama import Fore

dp = Dispatcher()

async def init():
    global TOKEN, CHAT_ID
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = int(os.getenv('TELEGRAM_CHAT_ID'))

async def start():
    global bot
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

@dp.startup()
async def startup():
    me = await bot.get_me()
        
    logger.info(f'@{me.username} has ready!')

# == channel ==
async def edit_title(chat_id: int, title: int):
    await bot.set_chat_title(chat_id, title)
    logger.trace("Chat title updated.")

async def edit_photo(chat_id: int, large_image: BufferedInputFile):
    await bot.set_chat_photo(chat_id, large_image)
    logger.trace("Chat photo updated.")

# == message ==
async def send_message(chat_id: int, text: str, media: BufferedInputFile = None) -> int:
    ret_msg = None
    if media:
        ret_msg = await bot.send_photo(chat_id, media, caption=text, disable_notification=True, parse_mode=ParseMode.HTML)
        logger.trace("Message with photo has been sent.")
    else:
        ret_msg = await bot.send_message(chat_id, text, disable_notification=True, parse_mode=ParseMode.HTML)
        logger.trace("Message has been sent.")
    return ret_msg.message_id

async def edit_caption(chat_id: int, message_id: int, text: str, media: BufferedInputFile = None):
    if media:
        input_media = InputMediaPhoto(media=media)
        await bot.edit_message_media(input_media, chat_id=chat_id, message_id=message_id)
        logger.trace("Message photo has been edited.")
    await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, parse_mode=ParseMode.HTML)
    logger.trace("Message caption has been edited.")

async def edit_text(chat_id: int, message_id: int, text: str):
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode=ParseMode.HTML)
    logger.trace("Message text has been edited.")

async def delete_message(chat_id: int, message_id: int):
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    logger.trace("Message has been removed.")

# == message ==
@dp.channel_post()
async def channel_post(message: Message):
    triggers = [message.new_chat_photo, message.new_chat_title, message.delete_chat_photo]
    for t in triggers:
        if t:
            logger.trace(f"Channel message removed.")
            await message.delete()
            break