from models.activity import Activity
from services.bots import telegram
from services.events import events, AVATAR_UPDATED
from config import ACTIVITY_TITLES, ACT_NONE_TITLE
from loguru import logger
from utils import images
import hashlib

class Channel:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.last_avatar_hash = None
        self.last_title = None

    async def update(self, act: Activity):
        try:
            avatar_hash = hashlib.md5(str(act.assets.large_image_url).encode('utf-8')).hexdigest()
            if avatar_hash != self.last_avatar_hash:
                await telegram.edit_photo(self.chat_id, act.assets.get_large_image())
                await events.call(AVATAR_UPDATED)
                self.last_avatar_hash = avatar_hash

            title = self.get_title_with_type_prefix(act) + " " + act.name
            if title != self.last_title:
                await telegram.edit_title(self.chat_id, title)
                self.last_title = title
            
            logger.debug("Channel has been updated.")
        except Exception as ex:
            logger.error(ex)

    async def reset(self):
        try:
            await telegram.edit_title(self.chat_id, ACT_NONE_TITLE)
            await telegram.edit_photo(self.chat_id, images.get_empty_avatar())
        except Exception as ex:
            logger.error(ex)
        
        self.last_avatar_hash = None
        self.last_title = None

    def get_title_with_type_prefix(self, act: Activity):
        return ACTIVITY_TITLES[act.type]