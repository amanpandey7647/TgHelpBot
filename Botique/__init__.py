import os
import sys
from .services import *
import logging

import api_key

logging.basicConfig(level=logging.INFO)

BOTIQUE = Botique(
    "stdborg",
    plugin_path="stdplugins",
    connection_retries=None,
    api_id=api_key.id,
    api_hash=api_key.hash
)

BOTIQUE.run_until_disconnected()
