import asyncio
import dotenv, os, sys
from services.bots import discord
from services.bots import telegram
from models.channel import Channel
from models.activity import Activity
from models.message import Message
from services.events import events, RPC_UPDATED
from loguru import logger
from config import MESSAGE_TASK_INVERVAL

dotenv.load_dotenv() # load env

if (MESSAGE_TASK_INVERVAL < 5):
    logger.warning("The interval is too low. A timeout from Telegram is possible!")

# == tasks ==
async def discord_task():
    await discord.init()
    await asyncio.gather(
        discord.start_client(), # start bot
        discord.watcher_loop() # rpc watcher
    )

async def telegram_task():
    global channel, message
    await telegram.init()
    channel = Channel(telegram.CHAT_ID) # channel object
    message = Message(telegram.CHAT_ID) # message object
    await telegram.start()

# == handlers ==
@events.on_call(RPC_UPDATED)
async def on_call(act: Activity):
    if act is None:
        await channel.reset()
        await message.pause()
    else:
        await channel.update(act)
        await message.run_task(act)

# == main ==
async def main():
    tasks = [
        discord_task(),
        telegram_task()
    ]
    await asyncio.gather(*tasks)

if (os.getenv('ENABLE_TRACE_LOGGING') == 'true'):
    logger.remove()
    logger.add(sys.stderr, level="TRACE")

if __name__ == '__main__':
    asyncio.run(main())