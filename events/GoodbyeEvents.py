import discord
from discord.ext import commands
import logging

from utils.utils import DataBase

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class GoodbyeEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, user):
        try:
            guild = user.guild
            goodbyetoggle2 = DataBase.db5.find_one({"guild_id": guild.id})['goodbyeembedtoggle']

            goodbyetoggle1 = DataBase.db5.find_one({"guild_id": guild.id})['goodbyetoggle']
            channel1 = DataBase.db5.find_one({"guild_id": guild.id})['channel']
            message1 = DataBase.db5.find_one({"guild_id": guild.id})['message']

            if goodbyetoggle2 == 'Enabled':
                
                channel = DataBase.db5.find_one({"guild_id": guild.id})['channel']
                message = DataBase.db5.find_one({"guild_id": guild.id})['message']
                title = DataBase.db5.find_one({"guild_id": guild.id})['title']
                colorr = DataBase.db5.find_one({"guild_id": guild.id})['color']
                color = int(colorr, 0)

                if "{user.id}" in message:
                        message = message.replace("{user.id}", "%s" % (user.id))
                if "{user.mention}" in message:
                    message = message.replace("{user.mention}", "%s" % (user.mention))
                if "{user.tag}" in message:
                    message = message.replace("{user.tag}", "%s" % (user.discriminator))
                if "{user.name}" in message:
                    message = message.replace("{user.name}", "%s" % (user.name))
                if "{user.avatar}" in message:
                    message = message.replace("{user.avatar}", "%s" % (user.avatar_url))
                if "{server.name}" in message:
                    message = message.replace("{server.name}", "%s" % (user.guild.name)) 
                if "{server.membercount}" in message:
                    message = message.replace("{server.membercount}", "%s" % (user.guild.member_count))          
                if "{server.icon}" in message:
                    message = message.replace("{server.icon}", "%s" % (user.guild.icon_url))

                if "{user.id}" in title:
                        title = title.replace("{user.id}", "%s" % (user.id))
                if "{user.mention}" in title:
                    title = title.replace("{user.mention}", "%s" % (user.mention))
                if "{user.tag}" in title:
                    title = title.replace("{user.tag}", "%s" % (user.discriminator))
                if "{user.name}" in title:
                    title = title.replace("{user.name}", "%s" % (user.name))
                if "{user.avatar}" in title:
                    title = title.replace("{user.avatar}", "%s" % (user.avatar_url))
                if "{server.name}" in title:
                    title = title.replace("{server.name}", "%s" % (user.guild.name)) 
                if "{server.membercount}" in title:
                    title = title.replace("{server.membercount}", "%s" % (user.guild.member_count))          
                if "{server.icon}" in title:
                    title = title.replace("{server.icon}", "%s" % (user.guild.icon_url))

                if title == None:
                    embed=discord.Embed(description=f"{message}", color=color)
                    channelsend = self.client.get_channel(channel)
                    await channelsend.send(embed=embed)
                    return
        
                if message == None:
                    embed=discord.Embed(title=f"{title}", color=color)
                    channelsend = self.client.get_channel(channel)
                    await channelsend.send(embed=embed)
                    return

                if message and title == None:
                    channelsend = self.client.get_channel(channel)
                    await channelsend.send(message)
                    return

                embed=discord.Embed(title=f'{title}', description=f"{message}", color=color)
                channelsend = self.client.get_channel(channel)
                await channelsend.send(embed=embed)
                return

            if goodbyetoggle1 == 'Enabled':
                message = DataBase.db5.find_one({"guild_id": guild.id})['message']
                title = DataBase.db5.find_one({"guild_id": guild.id})['title']
                colorr = DataBase.db5.find_one({"guild_id": guild.id})['color']
                color = int(colorr, 0)

                if "{user.id}" in message:
                        message = message.replace("{user.id}", "%s" % (user.id))
                if "{user.mention}" in message:
                    message = message.replace("{user.mention}", "%s" % (user.mention))
                if "{user.tag}" in message:
                    message = message.replace("{user.tag}", "%s" % (user.discriminator))
                if "{user.name}" in message:
                    message = message.replace("{user.name}", "%s" % (user.name))
                if "{user.avatar}" in message:
                    message = message.replace("{user.avatar}", "%s" % (user.avatar_url))
                if "{server.name}" in message:
                    message = message.replace("{server.name}", "%s" % (user.guild.name)) 
                if "{server.membercount}" in message:
                    message = message.replace("{server.membercount}", "%s" % (user.guild.member_count))          
                if "{server.icon}" in message:
                    message = message.replace("{server.icon}", "%s" % (user.guild.icon_url))

                if "{user.id}" in title:
                        title = title.replace("{user.id}", "%s" % (user.id))
                if "{user.mention}" in title:
                    title = title.replace("{user.mention}", "%s" % (user.mention))
                if "{user.tag}" in title:
                    title = title.replace("{user.tag}", "%s" % (user.discriminator))
                if "{user.name}" in title:
                    title = title.replace("{user.name}", "%s" % (user.name))
                if "{user.avatar}" in title:
                    title = title.replace("{user.avatar}", "%s" % (user.avatar_url))
                if "{server.name}" in title:
                    title = title.replace("{server.name}", "%s" % (user.guild.name)) 
                if "{server.membercount}" in title:
                    title = title.replace("{server.membercount}", "%s" % (user.guild.member_count))          
                if "{server.icon}" in title:
                    title = title.replace("{server.icon}", "%s" % (user.guild.icon_url))
                channel1 = DataBase.db5.find_one({"guild_id": guild.id})['channel']
                channelsend = self.client.get_channel(channel1)
                await channelsend.send(message)

        except Exception:
            pass

def setup(client):
    client.add_cog(GoodbyeEvents(client))