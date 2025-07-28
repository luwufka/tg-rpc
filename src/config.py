from discord import ActivityType

RPC_WATCHER_INTERVAL = 1000 # interval between requests (ms)
MESSAGE_TASK_INVERVAL = 5 # interval between requests (s)
MAX_ASSET_CACHE_SIZE = 4 # maximum size of assets cache (mb)

DISCORD_PROXY = "" # example: http://127.0.0.1:2080

ACTIVITY_TITLES = {
    ActivityType.playing: "🎮 Playing",
    ActivityType.listening: "🎵 Listening to",
    ActivityType.watching: "📺 Watching"
}

ACT_NONE_TITLE = "No activity . . ." # channel name when activity is None

SORT_ACTIVITIES = True # sorting, prioritizes activity with the game
LOGGING_ACTIVITY_DICTIONARY = True # write activity dictionary to log (only trace level)