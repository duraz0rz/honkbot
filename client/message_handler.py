from channel_role_setter import ChannelRoleSetter
from youtube_searcher import YoutubeSearcher


class MessageHandler:

    def __init__(self, discord_client, dependencies):
        self.command_list = [
            "!join",
            "!image",
            "!youtube",
            "!ranatalus",
            "!eamuse",
            "!help",
            "!insult",
            "!jacket",
            "!banner"
        ]

        self.client = discord_client
        self.channel_role_setter = dependencies["channel_role_setter"]
        self.youtube_searcher = dependencies["youtube_searcher"]
        self.google_images_searcher = dependencies["google_images_searcher"]
        self.insult_generator = dependencies["insult_generator"]
        self.speedrun_fetcher = dependencies["speedrun_fetcher"]
        self.eamuse_maintenance_minder = dependencies["eamuse_maintenance_minder"]
        self.remywiki_fetcher = dependencies["remywiki_fetcher"]

    def handle_message(self, message):
        if message.content.startswith('!test'):
            test = "test"
            await self.client.send_message(message.author, test)

        elif message.content.startswith('!join'):
            await self.channel_role_setter.set_role_for_user(message)

        elif message.content.startswith('!youtube'):
            await self.youtube_searcher.search_youtube(message)

        elif message.content.startswith('!image'):
            await self.google_images_searcher.search_google_images(message)

        elif message.content.startswith('!insult'):
            if len(message.content.lower().split(" ")) > 1:
                name = message.content.lower().split(" ")[1]
            else:
                await self.client.send_message(message.channel, "No one to insult :(")
                return
            await self.insult_generator.get_insult(message, name=name)

        elif message.content.startswith('!ranatalus'):
            await self.insult_generator.get_insult(message, name="ranatalus")

        elif message.content.startswith('!record'):
            await self.speedrun_fetcher.get_record(message)

        elif message.content.startswith('!eamuse'):
            await self.eamuse_maintenance_minder.get_eamuse_maintenance(message)

        elif message.content.startswith('!jacket'):
            await self.remywiki_fetcher.get_jacket(message)

        elif message.content.startswith('!banner'):
            await self.remywiki_fetcher.get_banner(message)

        elif "honk" in message.content.lower() and message.author != self.client.user:
            # HONK WINS AGAIN
            if "Skeeter" in message.author.name:
                await self.client.send_message(message.channel, "beep")
            else:
                await self.client.send_message(message.channel, "HONK!")

        elif message.content.startswith('!help'):
            await self.__print_help(message)
        elif message.content.startswith('!'):
            await self.__print_help(message)

    def __print_help(self, message):
        commands = "".join(["Commands are: ", ", ".join(self.command_list)])
        await self.client.send_message(message.channel, commands)
