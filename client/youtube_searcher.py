import requests

class YoutubeSearcher:

    def __init__(self, discord_client, google_api):
        self.client = discord_client
        self.google_api = google_api

    async def search_youtube(self, message):
        """
        Returns an video from youtube from the given search terms

        Requires:
            message (obj) - message object from discord object
        """

        if not self.google_api:
            await self.client.send_message(
                message.channel,
                "Sorry, cant do that right now! Ask your admin to enable"
            )
            return

        search = message.content.split(" ")
        del search[0]
        if search:
            query = " ".join(search)
            if len(query) < 250:
                google_url = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video"
                search_query = f"&q={query}&key={self.google_api}"
                r = requests.get(f"{google_url}{search_query}")
                try:
                    response = r.json()["items"][0]["id"]["videoId"]
                except IndexError:
                    await self.client.send_message(
                        message.channel,
                        f"Could not find any videos with search {query}"
                    )
                    return

                if response:
                    await self.client.send_message(message.channel, f"https://youtu.be/{response}")
                else:
                    await self.client.send_message(message.channel,
                                                   f"Could not find any videos with search {query}")
                    return
            else:
                await self.client.send_message(message.channel, "Query too long!")
                return
        else:
            await self.client.send_message(message.channel, "Usage: !youtube <search terms>")