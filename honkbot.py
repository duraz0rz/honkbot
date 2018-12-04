import sys
import logging
import discord
import os
import dotenv

from client.message_handler import MessageHandler
from client.channel_role_setter import ChannelRoleSetter
from client.youtube_searcher import YoutubeSearcher
from client.google_images_searcher import GoogleImagesSearcher
from client.insult_generator import InsultGenerator
from client.speedrun_fetcher import SpeedrunFetcher
from client.eamuse_maintenance_minder import EamuseMaintenanceMinder
from client.remywiki_fetcher import RemywikiFetcher

logging.basicConfig(stream=sys.stdout, level=logging.WARN)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Starting Honkbot...")


class Honkbot:
    """
    HONK

    A dumbass bot that interfaces with discord to do dumb stuff

    A list of things that it does:
    * Adds people to groups
    * Searches google for images
    * Searches youtube for videos
    * Insults people
    * Gives information on eAmuse downtime

    example:
        import honkbot
        bot = honkbot.Honkbot(discord_apikey)
        bot.run()
    """

    def __init__(self, discord_api, speedrun_api=None, google_api=None):
        self.discord_api = discord_api
        self.speedrun_api = speedrun_api
        self.google_api = google_api

        self.client = discord.Client()

        dependencies = {
            "channel_role_setter": ChannelRoleSetter(self.client),
            "youtube_searcher": YoutubeSearcher(self.client, google_api),
            "google_images_searcher": GoogleImagesSearcher(self.client, google_api),
            "insult_generator": InsultGenerator(self.client),
            "speedrun_fetcher": SpeedrunFetcher(self.client, speedrun_api),
            "eamuse_maintenance_minder": EamuseMaintenanceMinder(self.client),
            "remywiki_fetcher": RemywikiFetcher(self.client)
        }
        self.message_handler = MessageHandler(self.client, dependencies)

        self.on_ready = self.client.event(self.on_ready)
        self.on_message = self.client.event(self.on_message)

    def run(self):
        self.client.run(self.discord_api)

    # @self.client.event
    async def on_ready(self):
        logger.info('Logged in as {0} - {1}'.format(self.client.user.name, self.client.user.id))

    # @self.client.event
    async def on_message(self, message):
        await self.message_handler.handle_message(message)

if "__main__" in __name__:
    dotenv.load_dotenv()
    discord_api_key = os.getenv("DISCORD_API_KEY")
    speedrun_api_key = os.getenv("SPEEDRUN_API_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")

    bot = Honkbot(discord_api_key, speedrun_api_key, google_api_key)
    bot.run()
