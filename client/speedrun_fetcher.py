import requests


class SpeedrunFetcher:

    def __init__(self, discord_client, speedrun_api):
        self.client = discord_client
        self.speedrun_api = speedrun_api
        self.lastRecordSearch = ""

    async def get_record(self, message):
        """
        Accesses speedrun.com to get world record of given game

        Requires:
        message (obj) - message object from discord object
        """

        if not self.speedrun_api:
            await self.client.send_message(
                message.channel,
                "Sorry, cant do that right now! Ask your admin to enable"
            )
            return

        search = message.content.lower().split(" ")
        del search[0]
        if search:
            auth = {"Authorization": "Token {}".format(self.speedrun_api)}
            query = " ".join(search)
            results = []
            if len(search) < 100:
                base_url = "http://www.speedrun.com/api/v1/"
                api_next = "".join([base_url, "games?name={}".format(query)])
                while api_next:
                    r = requests.get(api_next, headers=auth)
                    for game in r.json()["data"]:
                        results.append(game)
                    next_page = ""
                    for page in r.json()["pagination"]["links"]:
                        if "next" in page['rel']:
                            next_page = page['uri']
                    api_next = next_page
                if results:
                    if query == self.lastRecordSearch:
                        results = [results[0]]
                    if len(results) == 1:
                        game_id = results[0]["id"]
                        r = requests.get("".join([base_url, "games/", game_id]), headers=auth)
                        game_name = r.json()['data']['names']['international']
                        r = requests.get(
                            "".join([base_url, "games/", game_id, "/categories"]), headers=auth)
                        game_category = ""
                        for category in r.json()['data']:
                            if category['name'].startswith('Any%'):
                                game_category = category
                                break
                        game_records_url = ""
                        if game_category:
                            for link in game_category['links']:
                                if "records" in link['rel']:
                                    game_records_url = link['uri']
                            r = requests.get(game_records_url, headers=auth)
                            run = r.json()['data'][0]['runs'][0]['run']
                            record = run['times']['realtime'][2:]
                            user_id = run['players'][0]['id']
                            r = requests.get("".join([base_url, "users/", user_id]), headers=auth)
                            user_name = r.json()['data']['names']['international']

                            await self.client.send_message(
                                message.channel,
                                f"The Any% record for {game_name} is {record} by {user_name}")

                        else:
                            await self.client.send_message(
                                message.channel,
                                "There are no Any% records for {}".format(game_name))
                    elif len(results) < 5:
                        names = []
                        for result in results:
                            names.append(result['names']['international'])
                        await self.client.send_message(
                            message.channel,
                            "Multiple results. Do a search for the following: {}".format(
                                ", ".join(names)))
                        await self.client.send_message(
                            message.channel,
                            "If you want the first result, redo the search")
                    else:
                        await self.client.send_message(
                            message.channel,
                            "Too many results! Be a little more specific")
                else:
                    await self.client.send_message(
                        message.channel,
                        "No games with that name found!")
            self.lastRecordSearch = query
        else:
            await self.client.send_message(
                message.channel,
                "You gotta give me a game to look for...")
