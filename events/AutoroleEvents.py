import discord
from discord.ext import commands
import logging

from utils.utils import Methods

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

client = discord.Client()
class AutoroleEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener("on_member_join")
    async def autorole_event(self, member):
        data = Methods.find_data(member.guild, "autoroles")
        for roleID in data:
            role = member.guild.get_role(roleID)
            await member.add_roles(role, reason="Asylum Auto-Role")

def setup(client):
    client.add_cog(AutoroleEvents(client))