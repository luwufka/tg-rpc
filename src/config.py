from discord import ActivityType

RPC_WATCHER_INTERVAL = 1000 # interval between requests (ms)
MESSAGE_TASK_INVERVAL = 5 # interval between requests (s)
MAX_ASSET_CACHE_SIZE = 4 # maximum size of assets cache (mb)
SORT_ACTIVITIES = True # sorting, prioritizes activity with the game
TRY_AGAIN_INTERVAL = 10 # try again on telegram api timeout (s)

ACTIVITY_TITLES = {
    ActivityType.playing: "🎮 Playing",
    ActivityType.listening: "🎵 Listening to",
    ActivityType.watching: "📺 Watching"
}
ACT_NONE_TITLE = "No activity . . ." # channel name when activity is None
DISCORD_PROXY = "" # example: http://127.0.0.1:2080
SPOTIFY_LOGO_URL = "https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Primary_Logo_RGB_Green.png"