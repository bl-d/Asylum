import discord
from discord.ext import commands
import discord
import logging
import aiohttp

from utils.botcache import BotCache

class AntiNuke(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.headers = {"Authorization": "Bot OTA1MTMzNzcwNzU4MzAzNzc1.YYFpgw.1zYUtG5irKYC6n2WAoQH2EcQnMs"}

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        try:
            reason = "asylum | antiban"
            logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
            logs = logs[0]
            user = logs.user.id
            Toggle = BotCache.antibantoggle.get(f'{guild.id}')
            Punishment = BotCache.antibanpunishment.get(f'{guild.id}')

            if Toggle == False:
                if Punishment == 'Ban':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
                if Punishment == 'Kick':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_member_kick(self, guild, user):
        try:
            reason = "asylum | antikick"
            logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
            logs = logs[0]
            user = logs.user.id
            Toggle = BotCache.antikicktoggle.get(f'{guild.id}')
            Punishment = BotCache.antikickpunishment.get(f'{guild.id}')

            if Toggle == False:
                if Punishment == 'Ban':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
                if Punishment == 'Kick':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        try:
            guild = channel.guild
            reason = "asylum | antichannel create"
            logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create).flatten()
            logs = logs[0]
            user = logs.user.id
            Toggle = BotCache.antichannelcreatetoggle.get(f'{guild.id}')
            Punishment = BotCache.antichannelcreatepunishment.get(f'{guild.id}')

            if Toggle == False:
                if Punishment == 'Ban':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
                if Punishment == 'Kick':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        try:
            guild = channel.guild
            reason = "asylum | antichannel delete"
            logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete).flatten()
            logs = logs[0]
            user = logs.user.id
            Toggle = BotCache.antichanneldeletetoggle.get(f'{guild.id}')
            Punishment = BotCache.antichanneldeletepunishment.get(f'{guild.id}')

            if Toggle == False:
                if Punishment == 'Ban':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
                if Punishment == 'Kick':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        try:
            guild = role.guild
            reason = "asylum | antirole create"
            logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create).flatten()
            logs = logs[0]
            user = logs.user.id
            Toggle = BotCache.antirolecreatetoggle.get(f'{guild.id}')
            Punishment = BotCache.antirolecreatetoggle.get(f'{guild.id}')

            if Toggle == False:
                if Punishment == 'Ban':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
                if Punishment == 'Kick':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        try:
            guild = role.guild
            reason = "asylum | antirole delete"
            logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete).flatten()
            logs = logs[0]
            user = logs.user.id
            Toggle = BotCache.antiroledeletetoggle.get(f'{guild.id}')
            Punishment = BotCache.antiroledeletetoggle.get(f'{guild.id}')

            if Toggle == False:
                if Punishment == 'Ban':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
                if Punishment == 'Kick':
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                        async with session.put("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                            else:
                                pass
        except Exception as error:
            print(error)

def setup(client):
    client.add_cog(AntiNuke(client))