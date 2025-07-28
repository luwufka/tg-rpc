from models.activity import Activity
from services.bots import telegram
from utils import formatter
from config import MESSAGE_TASK_INVERVAL
from loguru import logger
import asyncio, hashlib

class Message:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.message_id = None
        self.last_task = None
        self.last_img_hash = None

    async def run_task(self, act: Activity):
        if self.last_task:
            self.last_task.cancel()
        self.last_task = asyncio.create_task(self.handle(act))
        logger.debug("Message task has been started.")

    async def handle(self, act: Activity):
        try:
            while True:
                try:
                    if self.message_id is None:
                        self.message_id = await telegram.send_message(self.chat_id, formatter.get_message_text(act), act.assets.get_small_image())
                    else:
                        if act.assets.small_image_url:
                            img_hash = hashlib.md5(str(act.assets.small_image_url).encode('utf-8')).hexdigest()
                            if self.last_img_hash != img_hash:
                                await telegram.edit_caption(self.chat_id, self.message_id, formatter.get_message_text(act), act.assets.get_small_image())
                                self.last_img_hash = img_hash
                            else:
                                await telegram.edit_caption(self.chat_id, self.message_id, formatter.get_message_text(act))
                        else:
                            await telegram.edit_text(self.chat_id, self.message_id, formatter.get_message_text(act))
                            self.last_img_hash = None
                except Exception as ex:
                    logger.error(ex)
                    if self.message_id is not None:
                        try: await telegram.delete_message(self.chat_id, self.message_id)
                        except: pass
                        self.message_id = await telegram.send_message(self.chat_id, formatter.get_message_text(act), act.assets.get_small_image())

                await asyncio.sleep(MESSAGE_TASK_INVERVAL)
        except:
            pass