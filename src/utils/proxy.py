import os, dotenv

dotenv.load_dotenv() # import .env

def get_proxy():
    proxy_str = os.getenv('DISCORD_PROXY')
    if not proxy_str:
        return ""
    return proxy_str
    
DISCORD_PROXY = get_proxy()