from aiogram.types import BufferedInputFile
from loguru import logger
from colorama import Fore
from config import MAX_ASSET_CACHE_SIZE
from PIL import Image
import requests, hashlib, sys, io
from utils.proxy import DISCORD_PROXY

cache = {}

def ret_bif(url: str, resize: bool = False) -> BufferedInputFile:
    if sys.getsizeof(cache) / 1024 >= MAX_ASSET_CACHE_SIZE:
        logger.debug("Clearing cache . . .")
        cache.clear()
    
    HASH = hashlib.md5(url.encode()).hexdigest()

    if HASH in cache and cache[HASH]['isResized'] == resize:
        logger.trace(f"Using cached image for: {Fore.WHITE}{url}")
        return cache[HASH]['file']
    
    response = requests.get(url, proxies={"http": DISCORD_PROXY, "https": DISCORD_PROXY})

    if response.status_code != 200:
        logger.error(f"Failed to download asset {Fore.WHITE}[Code: {response.status_code}]")
        return None
    elif response.status_code == 200:
        logger.trace(f"Image downloaded! URL: {Fore.WHITE}{url}")
    
    CONTENT = io.BytesIO(response.content)

    image = Image.open(CONTENT)

    if resize:
        image = resize_img(image)
    
    background = create_bg(image)
    background.paste(image, (0, 0), image.convert("RGBA").split()[3])
    
    ret = io.BytesIO()
    background = background.convert("RGB")
    background.save(ret, format="JPEG")
    ret.seek(0)
    
    cache[HASH] = {'file': BufferedInputFile(ret.getvalue(), filename="rpc_asset.jpg"), 'isResized': resize}
    return cache[HASH]['file']

def resize_img(image: Image, size: tuple = (512, 512)) -> Image:
    w, h = image.size
    if (w, h) < size:
        image = image.resize(size, Image.Resampling.BICUBIC)
    return image

def create_bg(image: Image) -> Image:
    avg_color = get_avg_color(image)
    darker_color = tuple(int(c * 0.6) for c in avg_color)
    background = Image.new("RGB", image.size, darker_color)
    return background

def get_avg_color(image: Image) -> tuple:
    image = image.convert("RGB")
    pixels = list(image.getdata())
    avg_r = sum([pixel[0] for pixel in pixels]) // len(pixels)
    avg_g = sum([pixel[1] for pixel in pixels]) // len(pixels)
    avg_b = sum([pixel[2] for pixel in pixels]) // len(pixels)
    return (avg_r, avg_g, avg_b)

def get_empty_avatar() -> BufferedInputFile:
    avatar = Image.new("RGB", (720, 720), "#111111")
    ret = io.BytesIO()
    avatar.save(ret, format="JPEG")
    ret.seek(0)
    return BufferedInputFile(ret.getvalue(), filename="empty.jpg")