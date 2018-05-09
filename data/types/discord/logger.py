from data.types.bot.exceptions import LoggingError
from data.types.discord.embeds import LogEmbeds
from data.types.bot.config import Config

from time import sleep

import json
import sys


class Log:

    def load_responses():
        with open("data/logger_responses.json", 'r') as file:
            return json.load(file)



    def push(api_client, text=None, level="guild", g_ID=None):
        pass