import discord
from discord.ext import commands
import logging
from discord_webhook import DiscordWebhook, DiscordEmbed

from utils.utils import DataBase
from utils.botcache import BotCache


logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

client = discord.Client()
class ReadyEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):

        for server in self.client.guilds:

            if not DataBase.db1.find_one({ "guild_id": server.id }):
                DataBase.ServerSystem(server.id)
                logging.info(f'Created ServerSystem DB For {server.name}')
            if not DataBase.db3.find_one({ "guild_id": server.id }):
                DataBase.WelcomeSystem(server.id)
                logging.info(f'Created WelcomeSystem DB For {server.name}')
            if not DataBase.db5.find_one({ "guild_id": server.id }):
                DataBase.GoodbyeSystem(server.id)
                logging.info(f'Created GoodbyeSystem DB For {server.name}')
            if not DataBase.db6.find_one({ "guild_id": server.id }):
                DataBase.AntiNukeSystem(server.id)
                logging.info(f'Created AntiNukeSystem DB For {server.name}')
        logging.info(f"Connected To {self.client.user}")
        logging.info(f'Loaded with {len(set(self.client.walk_commands()))} commands')
        await self.client.change_presence(activity=discord.Streaming(name=f"solo.to/asylumbot", url="https://www.twitch.tv/discord"))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        server = self.client.get_guild(guild.id)
        if DataBase.db1.find_one({ "guild_id": server.id }):
            logging.info(f'Joined server with ServerSystem Already: {server.name}')
        else:
            DataBase.ServerSystem(server.id)
            logging.info(f'Created ServerSystem DB For {server.name}')
        if DataBase.db3.find_one({ "guild_id": server.id }):
            logging.info(f'Joined server with WelcomeSystem Already: {server.name}')
        else:
            DataBase.WelcomeSystem(server.id)
            logging.info(f'Created WelcomeSystem DB For {server.name}')
        if DataBase.db5.find_one({ "guild_id": server.id }):
            logging.info(f'Joined server with GoodbyeSystem Already: {server.name}')
        else:
            DataBase.GoodbyeSystem(server.id)
            logging.info(f'Created GoodbyeSystem DB For {server.name}')
        if DataBase.db6.find_one({ "guild_id": server.id }):
            logging.info(f'Joined server with AntiNukeSystem Already: {server.name}')
        else:
            DataBase.AntiNukeSystem(server.id)
            logging.info(f'Created AntiNukeSystem DB For {server.name}')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        for channel in guild.text_channels:
            webhook = DiscordWebhook(
                url="https://discord.com/api/webhooks/863814492064448526/N3Fes8OJscTuUewu0zxzjncur74kBrCotD4Iizy_j6kOYDCmaFNGIaKzvuz_zBuRVK6U")
            log = DiscordEmbed(title=f"Left A Server",description=f"Name: **{guild.name}**\nOwner: **{guild.owner}**\nMembers: **{len(guild.members)}**\n **clientinfo**\n users: {len(set(self.client.get_all_members()))}\n servers: {len(self.client.guilds)}", color=0x747f8d)
            webhook.add_embed(log)
            webhook.execute()
            break

def setup(client):
    client.add_cog(ReadyEvents(client))