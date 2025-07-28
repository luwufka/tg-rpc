import discord
import asyncio
import os
import hashlib
from config import RPC_WATCHER_INTERVAL, SORT_ACTIVITIES, DISCORD_PROXY, LOGGING_ACTIVITY_DICTIONARY
from loguru import logger
from services.events import events, RPC_UPDATED
from colorama import Fore
from models.activity import Activity

intents = discord.Intents.default()
intents.presences = True
intents.guilds = True
intents.members = True
intents.message_content = True

last_rpc_hash = None

ready_event = asyncio.Event()
async def init():
    global GUILD_ID, MEMBER_ID, RPC_WATCHER_INTERVAL, BOT_TOKEN, client
    # init env
    GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))
    MEMBER_ID = int(os.getenv('DISCORD_MEMBER_ID'))
    BOT_TOKEN = os.getenv('DISCORD_TOKEN')
    # init client
    if DISCORD_PROXY:
        logger.info("* Init with proxy.")
        client = discord.Client(intents=intents, proxy=DISCORD_PROXY)
    else:
        client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        logger.info(f'{client.user.name} has ready!')
        ready_event.set()

async def watcher_loop():
    global last_rpc_hash
    await ready_event.wait()
    
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        logger.error(f'Guild {Fore.WHITE}[ID: {GUILD_ID}]{Fore.RED} not found!')
        return
    
    member = guild.get_member(MEMBER_ID)
    if member is None:
        logger.error(f'Member {Fore.WHITE}[ID: {MEMBER_ID}]{Fore.RED} not found!')
        return
    
    ALLOWED_TYPES = [discord.ActivityType.playing, discord.ActivityType.listening, discord.ActivityType.watching]

    while True:
        acts = member.activities

        if acts:
            if SORT_ACTIVITIES: # sort acts
                if SORT_ACTIVITIES:
                    acts = sorted(acts, key=lambda activity: (ALLOWED_TYPES.index(activity.type) if activity.type in ALLOWED_TYPES else len(ALLOWED_TYPES)))
            for act in acts:
                if act.type in ALLOWED_TYPES:
                    rpc_hash = hashlib.md5(str(act.to_dict()).encode('utf-8')).hexdigest()

                    if rpc_hash != last_rpc_hash:
                        last_rpc_hash = rpc_hash
                        logger.debug(f"RPC Updated! {Fore.WHITE}[{Fore.YELLOW}{act.name} - {act.details}{Fore.WHITE}]")

                        ret_act = Activity(act)
                        if LOGGING_ACTIVITY_DICTIONARY:
                            logger.trace(str(act.to_dict()))
                        await events.call(RPC_UPDATED, ret_act)
                    break
                
        await asyncio.sleep(RPC_WATCHER_INTERVAL / 1000)

async def start_client():
    await client.start(BOT_TOKEN)