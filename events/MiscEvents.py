import discord
from discord.ext import commands
import logging
import json

from utils.utils import Customize

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class MiscEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener(name="on_message")
    async def on_afk_say(self, message):
        if message.guild:
            with open('utils/afk.json', 'r') as f:
                afks = json.load(f)
            try:
                if afks[str(message.author.id)]:
                    embed=discord.Embed(description=f"Welcome back, I have removed your **AFK** status", color=Customize.color)
                    await message.channel.send(embed=embed)
                    afks.pop(str(message.author.id))
                    with open('utils/afk.json', 'w') as f:
                        json.dump(afks, f, indent=4)
            except KeyError:
                pass
            
    @commands.Cog.listener(name="on_message")
    async def on_afk_ping(self, message):
        if len(message.mentions):
            with open('utils/afk.json', 'r') as f:
                afks = json.load(f)
            for i in message.mentions:
                if str(i.id) in afks and message.author != message.guild.me:
                    embed=discord.Embed(description=f'**{i.display_name}** is afk with the status: **{afks[str(i.id)]["message"]}**', color=Customize.color)
                    await message.channel.send(embed=embed)

def setup(client):
    client.add_cog(MiscEvents(client))