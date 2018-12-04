import discord
from discord.utils import Forbidden

class ChannelRoleSetter:

    def __init__(self, discord_client):
        self.client = discord_client

    async def set_role_for_user(self, message):
        """
        Sets a role to a user based on the given input

        Requires:
            message (obj) - message object from discord object
        """

        allowed_roles = ['OH', 'MI', 'KY', 'PA', 'IN', 'NY']
        if len(message.content.split(" ")) != 2:
            await self.client.send_message(
                message.channel, "".join(["Usage: !join [", ", ".join(allowed_roles), "]"]))
            return
        role = message.content.split(" ")[1]
        if role not in allowed_roles:
            await self.client.send_message(
                message.channel, "".join(["Allowed roles are: ", ", ".join(allowed_roles)]))
        else:
            role_object = discord.utils.get(message.server.roles, name=role)
            try:
                if message.author.roles:
                    await self.client.replace_roles(message.author, role_object)
                else:
                    await self.client.add_roles(message.author, role_object)
                await self.client.send_message(
                    message.channel, "Adding {0} to {1}".format(message.author.name, role))
            except Forbidden:
                await self.client.send_message(
                    message.channel, "I do not have permissions to assign roles right now. Sorry!")