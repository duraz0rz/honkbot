import requests


class GoogleImagesSearcher:

    def __init__(self, discord_client, google_api):
        self.client = discord_client
        self.google_api = google_api

    async def search_google_images(self, message):
        """
        Returns an image from google from the given search terms

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
            if len(query) < 150:
                cx_id = "009855409252983983547:3xrcodch8sc"
                url = (
                    f"https://www.googleapis.com/customsearch/v1?q={search}" +
                    f"&cx={cx_id}&searchType=image" + f"&key={self.google_api}"
                )
                r = requests.get(url)
                try:
                    response = r.json()["items"][0]["link"]
                    await self.client.send_message(message.channel, response)
                except KeyError:
                    await self.client.send_message(message.channel,
                                                   f"No results found for {query} :(")
            else:
                await self.client.send_message(message.channel, "Query too big!")
        else:
            await self.client.send_message(message.channel, "Usage: !image <search term>")
