from discord import ActivityType

RPC_WATCHER_INTERVAL = 1000 # interval between requests (ms)
SORT_ACTIVITIES = True # sorting, prioritizes activity with the game
MAX_ASSET_CACHE_SIZE = 4 # maximum size of assets cache (mb)
DISCORD_PROXY = ""
ACTIVITY_TITLES = {
    ActivityType.playing: "🎮 Playing",
    ActivityType.listening: "🎵 Listening to",
    ActivityType.watching: "📺 Watching"
}
LOGGING_ACTIVITY_DICTIONARY = True
MESSAGE_TASK_INVERVAL = 5 # interval between requests (s)