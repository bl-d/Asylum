import json
import random
import textwrap
import asyncio
import logging
import math
import os
import traceback
from urllib.request import Request, urlopen
from jishaku.cog import *
import discord

from utils.utils import Methods
from utils.help import AsylumHelp
from utils.botcache import BotCache
from utils.database import DataBase
from utils.paginator import *
from utils.utils import *
import pymongo
import asyncio
import base64
import binascii
import inspect
import io
import json
import re
import textwrap
import traceback
import urllib

from contextlib import redirect_stdout
from io import BytesIO
from random import choice
from typing import Optional
from typing import Union
from urllib.request import Request, urlopen

import discord
import pymongo
from PIL import Image
from discord.ext import commands
from discord.ext import commands, tasks
from discord_webhook import DiscordWebhook, DiscordEmbed
from io import BytesIO

import aiohttp
import discord
import inspect
import giphy_client
import pymongo
import requests
from PIL import Image
import logging
from discord import Embed
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from giphy_client.rest import ApiException
from utils.utils import DataBase
from utils.utils import Methods
from utils.utils import Checks


logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

client = discord.Client()
class InternalSystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='reload', aliases=['rl'])
    @commands.is_owner()
    async def reload(self, ctx, cog):
        try:
            self.client.unload_extension(f"cogs.{cog}")
            self.client.load_extension(f"cogs.{cog}")
            await ctx.message.reply(embed=Methods.create_embed(f'**{cog}** has been reloaded'))
        except commands.ExtensionNotLoaded as e:
            await ctx.message.reply(embed=Methods.create_embed(f'**{cog}** is not loaded'))

    @commands.command(name="unload", aliases=['ul']) 
    @commands.is_owner()
    async def unload(self, ctx, cog):
        try:
            self.client.unload_extension(f"cogs.{cog}")
            await ctx.message.reply(embed=Methods.create_embed(f'**{cog}** is not loaded'))
        except commands.ExtensionNotLoaded as e:
            await ctx.message.reply(embed=Methods.create_embed(f'**{cog}** has not been found'))

    @commands.command(name="load")
    @commands.is_owner()
    async def load(self, ctx, cog):
        try:
            self.client.load_extension(f"cogs.{cog}")
            await ctx.message.reply(embed=Methods.create_embed(f'**{cog}** has been loaded'))
        except commands.errors.ExtensionNotFound:
            await ctx.message.reply(embed=Methods.create_embed(f'**{cog}** is not loaded'))

    @commands.command()
    @commands.is_owner()
    async def reloadall(self, ctx, cog=None):
        if not cog:
            async with ctx.typing():
                message = await ctx.send("Reloading all cogs")
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.client.unload_extension(f"cogs.{ext[:-3]}")
                            self.client.load_extension(f"cogs.{ext[:-3]}")
                            message = await ctx.send(f"Reloaded: `{ext}`\n")
                        except Exception as e:
                            message = await ctx.send(f"Failed to reload: `{ext}`")
        else:
            async with ctx.typing():
                message = await ctx.send("Reloading all cogs")
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    message = await ctx.send(f"Failed to reload: `{ext}`\n This cog doesnt exist g")
                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.client.unload_extension(f"cogs.{ext[:-3]}")
                        self.client.load_extension(f"cogs.{ext[:-3]}")
                        message = await ctx.send(f"Reloaded: `{ext}`\n")
                    except Exception:
                        desired_trace = traceback.format_exc()
                        message = await ctx.send(f"Failed to reload: `{ext}`\n{desired_trace}")
                await ctx.send(message)

    @commands.command(name="listcogs", aliases=['lc'])
    @commands.is_owner()
    async def listcogs(self, ctx):
        cogs = '\n'.join([str(cog) for cog in self.client.extensions])
        message = f"Loaded cogs:```css\n{cogs}```"
        await ctx.message.reply(message)

    @commands.command(name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body):
        if ctx.author.id in [815203787253350436, 831171302336757790]:
            env = {
                'ctx': ctx,
                'client': self.client,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                'source': inspect.getsource
            }

            def cleanup_code(content):
                if content.startswith('```') and content.endswith('```'):
                    return '\n'.join(content.split('\n')[1:-1])
                return content.strip('` \n')

            env.update(globals())

            body = cleanup_code(body)
            stdout = io.StringIO()
            err = out = None

            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

            def paginate(text: str):
                '''Simple generator that paginates text.'''
                last = 0
                pages = []
                for curr in range(0, len(text)):
                    if curr % 1980 == 0:
                        pages.append(text[last:curr])
                        last = curr
                        appd_index = curr
                if appd_index != len(text)-1:
                    pages.append(text[last:curr])
                return list(filter(lambda a: a != '', pages))
            
            try:
                exec(to_compile, env)
            except Exception as e:
                err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
                return await ctx.message.add_reaction('\u2049')

            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                if ret is None:
                    if value:
                        try:
                            
                            out = await ctx.send(f'```py\n{value}\n```')
                        except:
                            paginated_text = paginate(value)
                            for page in paginated_text:
                                if page == paginated_text[-1]:
                                    out = await ctx.send(f'```py\n{page}\n```')
                                    break
                                await ctx.send(f'```py\n{page}\n```')
                else:
                    try:
                        out = await ctx.send(f'```py\n{value}{ret}\n```')
                    except:
                        paginated_text = paginate(f"{value}{ret}")
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')

            if out:
                await ctx.message.add_reaction('\u2705')  # tick
            elif err:
                await ctx.message.add_reaction('\u2049')  # x
            else:
                await ctx.message.add_reaction('\u2705')
        else:
            return

    @commands.command()
    @commands.is_owner()
    async def servers(self, ctx):
        page = 1
        msg = "\n".join(["`{} - {}` - {} members".format(x.name, x.id, x.member_count) for x in sorted(sorted(self.client.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count,reverse=True)][0:20])
        s=discord.Embed(description=msg, colour=0xffffff)
        s.set_author(name="Servers ({})".format(len(self.client.guilds)))
        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(self.client.guilds))) / 20)))
        message = await ctx.send(embed=s)
        await message.add_reaction("◀")
        await message.add_reaction("▶")
        def reactioncheck(reaction, user):
            if user == ctx.author:
                if reaction.message.id == message.id:
                    if reaction.emoji == "▶" or reaction.emoji == "◀":
                        return True
        page2 = True
        while page2:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=reactioncheck)
                if reaction.emoji == "▶":
                    if page != math.ceil(len(list(set(self.client.guilds))) / 20):
                        page += 1
                        msg = "\n".join(["`{} - {}` - {} members".format(x.name, x.id, x.member_count) for x in sorted(sorted(self.client.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count,reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=0xffffff)
                        s.set_author(name="Servers ({})".format(len(self.client.guilds)))
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(self.client.guilds))) / 20)))
                        await message.edit(embed=s)
                    else:
                        page = 1
                        msg = "\n".join(["`{} - {}` - {} members".format(x.name, x.id, x.member_count) for x in sorted(sorted(self.client.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=0xffffff)
                        s.set_author(name="Servers ({})".format(len(self.client.guilds)))
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(self.client.guilds))) / 20)))
                        await message.edit(embed=s)
                if reaction.emoji == "◀":
                    if page != 1:
                        page -= 1
                        msg = "\n".join(["`{} - {}` - {} members".format(x.name, x.id, x.member_count) for x in sorted(sorted(self.client.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=0xffffff)
                        s.set_author(name="Servers ({})".format(len(self.client.guilds)))
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(self.client.guilds))) / 20)))
                        await message.edit(embed=s)
                    else:
                        page = math.ceil(len(list(set(self.client.guilds)))/ 20)
                        msg = "\n".join(["`{} - {}` - {} members".format(x.name, x.id, x.member_count) for x in sorted(sorted(self.client.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=0xffffff)
                        s.set_author(name="Servers ({})".format(len(self.client.guilds)))
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(self.client.guilds))) / 20)))
                        await message.edit(embed=s)
            except asyncio.TimeoutError:
                try:
                    await message.remove_reaction("◀", ctx.me)
                    await message.remove_reaction("▶", ctx.me)
                except:
                    pass
                page2 = False

    @commands.command()
    @commands.is_owner()
    async def leaveserver(self, ctx, id: int):
        guild = self.client.get_guild(id)
        await guild.leave()
        await ctx.message.reply(embed=Methods.create_embed(f'Left **{guild.name}**'))

    @commands.command()
    @commands.is_owner()
    async def getserver(self, ctx, id: int):
        output = ''
        guild = self.client.get_guild(id)
        if not guild:
            return await ctx.send("Unkown Guild ID")
        gn = guild.name
        gi = str(guild.id)
        gm = str(len(guild.members))
        go = str(guild.owner)
        output += f'<:AsylumArrowW:898012490506567711> `Name:` {gn}\n<:AsylumArrowW:898012490506567711> `ID:` {gi}\n<:AsylumArrowW:898012490506567711> `Members:` {gm}\n<:AsylumArrowW:898012490506567711> `Owner:` {go}'
        embed = discord.Embed(color=0xffffff,title=f'Guild Info For : {id}',description=output,)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def getuser(self, ctx, id: int):
        output = ''
        user = self.client.get_user(id)
        if not user:
            return await ctx.send("Unkown User ID")
        un = user.name
        ui = str(user.id)
        ug = ''
        ugc = 0
        guilds = self.client.guilds
        for guild in guilds:
            if guild.owner.id == id:
                ug += f"`{guild.name}`\n"
                ugc += 1
        if ug == '': ug = "**None.**"
        output += f'<:AsylumArrowW:898012490506567711> `Name:` {un}\n<:AsylumArrowW:898012490506567711> `ID:` {ui}\n<:AsylumArrowW:898012490506567711> `Servers:` {ugc}'
        embed = discord.Embed(color=0xffffff,title=f'User Info For {id}',description=output,)
        await ctx.send(embed=embed)

    @commands.group(name='blacklist')
    @commands.is_owner()
    async def blacklist(self, ctx):
        pass

    @blacklist.command(name='add')
    @commands.is_owner()
    async def blacklist_add(self, ctx, userid: int, level=1, *, reason=None):
        if DataBase.blacklist.find_one({'user_id': userid}):
            await ctx.send(embed=Methods.create_embed('User ID already blacklisted'))
        else:
            if self.client.get_user(userid) != None:
                getusername = await self.client.fetch_user(userid)
                DataBase.blacklist.insert_one({
                    'user_id': userid,
                    'user_tag': f"{getusername}",
                    'reason': reason
                })
                await ctx.send(embed=Methods.create_embed(f'<@{userid}> is now blacklisted'))
                try:
                    user = self.client.get_user(userid)
                    await user.send(embed=Methods.create_embed(f'**Alert**\nYou have been blacklisted from `Asylum`\nReason: `{reason}`\nIf you would like to appeal this Blacklist contact `Java#0009`'))
                except:
                    pass
            else:
                await ctx.send(embed=Methods.create_embed('Unknown User ID'))



    @blacklist.command(name='show')
    @commands.is_owner()
    async def blacklist_show(self, ctx, page: int = 1):
        output = ''
        embed = discord.Embed(color=0xffffff,title='**Blacklisted Users**',description=output,)
        blacklisted = DataBase.blacklist.find()
        pages = math.ceil(blacklisted.count()/10)
        if 1 <= page <= pages:
            counter = 1+(page-1)*10
            for _user in blacklisted[(page-1)*10:page*10]:
                _xa = await self.client.fetch_user(_user['user_id'])
                if _xa.mutual_guilds:
                    embed.add_field(name=f"**{counter}**. `{_user['user_tag']}`", value=f"<:AsylumArrowW:898012490506567711> ID: `{_user['user_id']}`\n<:AsylumArrowW:898012490506567711> Reason: `{_user['reason']}`",inline=False)
                else:
                    embed.add_field(name=f"**{counter}**. `{_user['user_tag']}`", value=f"ID: `{_user['user_id']}`\n<:AsylumArrowW:898012490506567711> Reason: `{_user['reason']}`\n<:AsylumArrowW:898012490506567711> User Does Not Share Any Mutual Servers.",inline=False)
                counter += 1
            embed.set_footer(text=f'Page {page} - {pages}')
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=Methods.create_embed('The specified page does not exist'))

    @blacklist.command(name='remove')
    @commands.is_owner()
    async def blacklist_remove(self, ctx, userid: int):
        if DataBase.blacklist.find_one({'user_id': userid}):
            DataBase.blacklist.delete_one({'user_id': userid})
            await ctx.send(embed=Methods.create_embed(f'<@{userid}> has been unblacklisted'))
        else:
            await ctx.send(embed=Methods.create_embed(f'<@{userid}> is not blacklisted'))

def setup(client):
    client.add_cog(InternalSystem(client))