from datetime import datetime
from config import SPOTIFY_LOGO_URL
import discord
import utils.images

class ActivityAssets:
    def __init__(self, large_image_url, small_image_url):
        self.large_image_url = large_image_url
        self.small_image_url = small_image_url

    def get_large_image(self):
        return utils.images.ret_bif(self.large_image_url, True)

    def get_small_image(self):
        if self.small_image_url is None:
            return None
        return utils.images.ret_bif(self.small_image_url)

class Activity:
    def __init__(self, act: discord.Activity | discord.Spotify):
        if isinstance(act, discord.Activity):
            self.name = act.name
            self.assets = ActivityAssets(act.large_image_url, act.small_image_url)
            self.type = act.type
            self.start_time = act.start
            self.end_time = act.end
            if (self.end_time):
                self.track_length = act.end - act.start
            self.details = act.details
            self.state = act.state
            self.large_text = act.assets.get("large_text", None)
            self.large_url = act.assets.get("large_url", None)
        elif isinstance(act, discord.Spotify):
            self.name = "Spotify"
            self.assets = ActivityAssets(act.album_cover_url, SPOTIFY_LOGO_URL)
            self.type = discord.ActivityType.listening
            self.start_time = act.start
            self.end_time = act.end
            if (self.end_time):
                self.track_length = self.end_time - self.start_time
            self.details = act._details
            self.state = act._state
            self.large_text = None
            self.large_url = None

    def format_time(self, total_seconds: int) -> str:
        days = total_seconds // (24 * 3600)
        hours = (total_seconds % (24 * 3600)) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if days > 0:
            return f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"
        elif hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

    def get_elapsed_time(self) -> str:
        if self.start_time is None:
            self.start_time = datetime.now()

        elapsed_time = datetime.now().timestamp() - self.start_time.timestamp()
        return self.format_time(int(elapsed_time))

    def get_track_length(self) -> str:
        total_seconds = self.track_length.total_seconds()
        return self.format_time(int(total_seconds))