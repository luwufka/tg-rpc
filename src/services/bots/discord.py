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

ALLOWED_TYPES = [discord.ActivityType.playing, discord.ActivityType.listening, discord.ActivityType.watching]
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

def get_valid_act(acts):
    if not acts:
        return None
    
    if SORT_ACTIVITIES:
        acts = sorted(acts, key=lambda act: (
            ALLOWED_TYPES.index(act.type) if act.type in ALLOWED_TYPES 
            else len(ALLOWED_TYPES)
        ))
    
    for act in acts:
        if act.type in ALLOWED_TYPES:
            return act
    
    return None

async def handle_act(act):
    global last_rpc_hash
    
    if act is None or act.large_image_url is None:
        if last_rpc_hash is not None:
            last_rpc_hash = None
            await events.call(RPC_UPDATED, None)
        return
    
    rpc_hash = hashlib.md5(str(act.to_dict()).encode('utf-8')).hexdigest()
    
    if rpc_hash != last_rpc_hash:
        last_rpc_hash = rpc_hash
        logger.debug(f"RPC Updated! [{act.name} - {act.details}]")
        
        if LOGGING_ACTIVITY_DICTIONARY:
            logger.trace(str(act.to_dict()))
            
        ret_act = Activity(act)
        await events.call(RPC_UPDATED, ret_act)

async def watcher_loop():
    global last_rpc_hash
    await ready_event.wait()
    
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        logger.error(f'Guild [ID: {GUILD_ID}] not found!')
        return
    
    member = guild.get_member(MEMBER_ID)
    if member is None:
        logger.error(f'Member [ID: {MEMBER_ID}] not found!')
        return
    
    while True:
        act = get_valid_act(member.activities)
        await handle_act(act)
        await asyncio.sleep(RPC_WATCHER_INTERVAL / 1000)

async def start_client():
    await client.start(BOT_TOKEN)