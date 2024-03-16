import asyncio
import importlib.util
import inspect
import logging
from pathlib import Path

from telethon import TelegramClient
import telethon.utils
import telethon.events


class ReverseList(list):
    def __iter__(self):
        return reversed(self)

class Botique(TelegramClient):
    def __init__(
            self, session, *, plugin_path="plugins", storage=None, admins=[],
            bot_token=None, **kwargs):
        # TODO: handle non-string session
        #
        # storage should be a callable accepting plugin name -> Storage object.
        # This means that using the Storage type as a storage would work too.
        self._name = session
        self.storage = storage or (lambda n: Storage(Path("data") / n))
        self._logger = logging.getLogger(session)
        self._plugins = {}
        self._plugin_path = plugin_path
        self.admins = admins

        kwargs = {
            "api_id": 6, "api_hash": "eb06d4abfb49dc3eeb1aeb98ae0f581e",
            **kwargs}
        super().__init__(session, **kwargs)

        self._event_builders = ReverseList()

        self.loop.run_until_complete(self._async_init(bot_token=bot_token))

