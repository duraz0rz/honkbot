import requests


class InsultGenerator:

    def __init__(self, discord_client):
        self.client = discord_client

    async def get_insult(self, message, name):
        """
        Returns a scathing insult about the given name

        Required:
        name (str) - name of person to insult
        """
        r = requests.get("http://quandyfactory.com/insult/json")
        insult = r.json()["insult"]
        await self.client.send_message(message.channel, insult.replace("Thou art", f"{name} is"))
