import asyncio
import math
from discord import Color, Member, Role
from typing import Union
from discord.ext.tasks import loop
from discord_webhook import DiscordWebhook, DiscordEmbed
import discord
from discord.ext import commands
import json
import time
import aiohttp, asyncio
import asyncio
import logging
import os
import signal
import typing
import random
from collections import OrderedDict
from pathlib import Path
import aiosqlite

import discord
import aiohttp
import motor.motor_asyncio
import tinydb
import mystbin
import newsapi
import asyncdagpi
import vacefron
import prsaw
import nomics
from discord.ext import commands



from typing import Union, Optional
from psutil import Process, virtual_memory

from utils.paginator import *
import asyncdagpi
from utils.utils import DataBase
from utils.utils import Customize
from utils.utils import Methods
from utils import arg

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.tasks = []

    @commands.command(help='Gets the color of said role')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rolecolor(self, ctx, *, color: Union[Color, Member, Role]):
        alias = ctx.invoked_with.lower()
        color = color if isinstance(color, Color) else color.color
        buffer = await self.bot.loop.run_in_executor(None, Methods.solid_color_image, color.to_rgb())
        file = discord.File(filename="color.png", fp=buffer)
        embed = Methods.embed_create(ctx, title=f'Info for {alias}:', color=color)
        embed.add_field(name='Hex:', value=f'`{color}`')
        embed.add_field(name='Int:', value=f'`{str(color.value).zfill(8)}`')
        embed.add_field(name='RGB:', value=f'`{color.to_rgb()}`')
        embed.set_thumbnail(url="attachment://color.png")
        await ctx.send(file=file, embed=embed)

    @commands.command(help='Sends all of the emojis in a server')
    async def serveremotes(self, ctx):
        msg = ""
        for x in ctx.guild.emojis:
            if x.animated:
                msg += "<a:{}:{}> ".format(x.name, x.id)
            else:
                msg += "<:{}:{}> ".format(x.name, x.id)
        if msg == "":
            await ctx.send("There are no emojis in this server g")
            return
        else:
            i = 0 
            n = 2000
            for x in range(math.ceil(len(msg)/2000)):
                while msg[n-1:n] != " ":
                    n -= 1
                s=discord.Embed(title=f"Emojis for {ctx.guild.name}",description=msg[i:n], color=Customize.color)
                i += n
                n += n
                await ctx.send(embed=s)

    @commands.command(help='Gets hte users id')
    async def userid(self, ctx, *, user: discord.Member=None):
        """Get someone userid"""
        author = ctx.message.author
        if not user:
            user = author
        await ctx.send("`{}`'s ID: `{}`".format(user, user.id))
        
    @commands.command(help='Gets the roles id')
    async def roleid(self, ctx, *, role: discord.Role):
        """Get a roles id"""
        await ctx.send("`{}`'s ID: `{}`".format(role.name, role.id))
    
    @commands.command(help='Gets the servers id')
    async def serverid(self, ctx):
        """Get the servers id"""
        server = ctx.guild
        await ctx.send("{}'s ID: `{}`".format(server.name, server.id))
        
    @commands.command(help='Gets the channels id')
    async def channelid(self, ctx, *, channel: str=None):
        """Get a channels id"""
        if not channel:
            channel = ctx.message.channel
        else:
            channel = Methods.get_text_channel(ctx, channel)
            if not channel:
                return await ctx.send("I could not find that channel g")
        await ctx.send("<#{}> ID: `{}`".format(channel.id, channel.id))

    @commands.command(usage="<reason>")
    async def afk(self, ctx, *, reason: str = 'No Reason'):
        with open('utils/afk.json', 'r') as f:
            afks = json.load(f)
        try:
            if afks[str(ctx.author.id)]:
                embed=discord.Embed(description=f"Welcome back, I have removed your **AFK** status", color=Customize.color)
                return await ctx.send(embed=embed)
        except KeyError:
            pass
        afks[str(ctx.author.id)] = {"message": reason}
        embed=discord.Embed(description=f'**{ctx.author.display_name}** is now AFK with the status: **{afks[str(ctx.author.id)]["message"]}**', color=Customize.color)
        await ctx.send(embed=embed)
        await asyncio.sleep(1)
        with open('utils/afk.json', 'w') as f:
            json.dump(afks, f, indent=4)

    @commands.command()
    async def boostcount(self, ctx):
        embed = discord.Embed(title = f'{ctx.guild.name}\'s Boost Count', description = f'{str(ctx.guild.premium_subscription_count)}', color=Customize.color)
        await ctx.send(embed = embed)

    @commands.command(name="firstmsg")
    async def firstmsg(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        first_message = (await channel.history(limit=1, oldest_first=True).flatten())[0]
        await ctx.send(f'{first_message.content} - {first_message.jump_url}')
    
    @commands.command(name="invites")
    async def invites(self, ctx, member: discord.Member = None):
        totalInvites = 0
        if member == None:
            member = ctx.author
        for i in await ctx.guild.invites():
            if i.inviter == member:
                totalInvites += i.uses
        if member == ctx.author:
             embed = discord.Embed(title="Invite Count", description="You've invited **`%s`** members to the server" % (totalInvites),color=Customize.color)
        else:
            embed = discord.Embed(title="invites", description="**`%s`** has invited **`%s`** members to the server" % (member.name, totalInvites), color=Customize.color)
        await ctx.send(embed=embed)

    @commands.command(name="joined-at")
    async def joinedat(self, ctx):
        joined = ctx.author.joined_at.strftime("%a, %d %b %Y %I:%M %p")
        await ctx.send(embed=discord.Embed(title="Join Date", description="**`%s`**" % (joined), color=Customize.color))

    @commands.command(
        name='avatar',
        aliases=['av', 'ab', 'ac', 'ah', 'pfp', 'avi', 'ico', 'icon'],
        help='get any discord user profile picture'
    )
    async def avatar(self, ctx, user: Optional[Union[discord.User, discord.Member]]):
        try:
            user = await self.bot.fetch_user(user.id)
        except AttributeError:
            user = ctx.author
        webp = user.avatar.replace(format='webp')
        jpg = user.avatar.replace(format='jpg')
        png = user.avatar.replace(format='png')
        avemb = discord.Embed(
            color=Customize.color,
            title=f"{user}'s Avatar",description=f"[**png**]({png}) - [**jpg**]({jpg}) - [**webp**]({webp})"
            if not user.avatar.is_animated()
            else f"[**png**]({png}) - [**jpg**]({jpg}) - [**webp**]({webp}) - [**gif**]({user.avatar.replace(format='gif')})"
        )
        avemb.set_image(url=user.avatar.url)
        await ctx.send(embed=avemb)

    @commands.command()
    async def servericon(self, ctx):
        server = ctx.guild
        webp = server.icon.replace(format='webp')
        jpg = server.icon.replace(format='jpg')
        png = server.icon.replace(format='png')
        avemb = discord.Embed(
            color=Customize.color,
            title=f"{server}'s Icon",description=f"[**png**]({png}) - [**jpg**]({jpg}) - [**webp**]({webp})"
            if not server.icon.is_animated()
            else f"[**png**]({png}) - [**jpg**]({jpg}) - [**webp**]({webp}) - [**gif**]({server.icon.replace(format='gif')})"
        )
        avemb.set_image(url=server.icon.url)
        await ctx.send(embed=avemb)

    @commands.command(help='Checks the permissions said user has', name='permissions')
    @commands.guild_only()
    async def permissions(self, ctx, *, member: discord.Member = None):
        channel = ctx.message.channel
        if member is None:
            member = ctx.message.author
        await Methods.say_permissions(ctx, member, channel)

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()

        await message.edit(content=f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")

    @commands.command(help='Shows information about the bot')
    async def botinfo(self, ctx):
        proc = Process()
        with proc.oneshot():
            commands = (len(self.bot.commands))
            total_members = sum(len(s.members) for s in ctx.bot.guilds)
            total_online = sum(1 for m in ctx.bot.get_all_members() if m.status != discord.Status.offline)
            unique_members = set(ctx.bot.get_all_members())
            unique_online = sum(1 for m in unique_members if m.status != discord.Status.offline)
            text = sum([len(guild.text_channels) for guild in ctx.bot.guilds])
            voice = sum([len(guild.voice_channels) for guild in ctx.bot.guilds])
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)
            mem_usage = mem_total * (mem_of_total / 100)
            channels = f'<:AsylumVersion:891451024420794378> Version: `0.1`\n<:AsylumStorage:891450424681459752> Total Storage: `{mem_usage:,.3f} MB`\n<:AsylumSupport:891451343825412216> Support Server: [here](https://discord.gg/n2fYsR2KMb)'
            members = f"<:AsylumGuilds:891449788057419846> Guilds: `{len(self.bot.guilds)}`\n<:AsylumUsers:891449330421071893> Users: `{total_members:,}`\n<:AsylumUsers:891449330421071893> Unique: `{len(unique_members):,}`"
        embed = discord.Embed(
            title=f'asylum info',color=Customize.color
        )
        embed.add_field(name="System",
                        value=channels,
                        inline=True)
        embed.add_field(name="Statistics",
                        value=members,
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(help='Gets the bots invite')
    async def invite(self, ctx):
        embed = discord.Embed(
            title=f'asylum invite',description=f"Thank you for your interest in Asylum, here you can find the invite, support server and documentation. You require the `Manage Server` permission to add bots to servers. If you don't have this permission make sure to ask someone who has it to add it.\n\nAsylum asks for the `Administrator` permission by default, if you dont want Asylum to have Admin, then simply un-tick the box. Be aware that Asylum may not work without certain permissions.\n\n[**Bot Invite**](https://discord.com/api/oauth2/authorize?client_id=881175401244819466&permissions=8&scope=bot)\n[**Support Server**](https://discord.gg/p9QNR6qNJU)\n[**Documentation**](https://discord.gg/p9QNR6qNJU)",color=Customize.color
        )
        await ctx.send(embed=embed)

    @commands.command(help='Gets the bots invite')
    async def support(self, ctx):
        embed = discord.Embed(
            title=f'asylum support',description=f"Hey! Below you can find the `Support Server` invite link, there you can ask any qeustions or concerns you have. If you have developmental/partnership offers please email `javalmao@riseup.net`.\n\n[**Bot Invite**](https://discord.com/api/oauth2/authorize?client_id=881175401244819466&permissions=8&scope=bot)\n[**Support Server**](https://discord.gg/p9QNR6qNJU)\n[**Documentation**](https://discord.gg/p9QNR6qNJU)",color=Customize.color
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, suggestion):
        channel = self.bot.get_channel(903789944944881665)
        msg = await channel.send(embed=discord.Embed(title=f"Suggestion by {ctx.message.author}",description=f"{suggestion}", color=Customize.color))
        await ctx.send('sent')
        await msg.add_reaction('<:AsylumCorrect:891704856660832266>')
        await msg.add_reaction('<:AsylumWrong:891703754703900702>')

    @commands.command()
    async def bug(self, ctx, bug):
        channel = self.bot.get_channel(904027111478677534)
        msg = await channel.send(embed=discord.Embed(title=f"Bug Reported by {ctx.message.author}",description=f"{bug}", color=Customize.color))
        await ctx.send('sent')
        await msg.add_reaction('<:AsylumCorrect:891704856660832266>')
        await msg.add_reaction('<:AsylumWrong:891703754703900702>')



    @commands.Cog.listener()
    async def on_command(self, ctx):
        await self.bot.wait_until_ready()
        try:
            webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/905610817733533736/FIFEyitR7JUIAJ-bOQmOHt-dFsTfGBnmlM-vDPA1PwBm214QOB87RNqJfwuZzosBmPSB")
            abusewatchlog = DiscordEmbed(title="Command Log", description=f"**User:** {ctx.author.name}#{ctx.author.discriminator} (`{ctx.author.id}`)\n**Guild:** {ctx.guild.name} (`{ctx.guild.id}`)\n**Channel:** {ctx.channel.mention} (`{ctx.channel.id}`)\n**Content:** {ctx.message.content} (`{ctx.message.id}`)",color=0xffffff)
            webhook.add_embed(abusewatchlog)
            webhook.execute()
        except:
            pass

    @commands.command(name="npm")
    async def npm(self, ctx, npm: str):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.popcat.xyz/npm?q={npm}") as r:
                data = await r.json()
                name = data['name']
                version = data['version']
                author = data['author']
                description = data['description']
                await ctx.send(embed=discord.Embed(title="NPM Package Information", description=f"**Name:** {name}\n**Version:** {version}\n**Author:** {author}\n```{description}```", color=Customize.color))

    @commands.command(name="instagram")
    async def instagram(self, ctx, song: str):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.popcat.xyz/instagram?user={song}") as r:
                data = await r.json()
                name = data['username']
                posts = data['posts']
                followers = data['followers']
                bio = data['biography']
                embed=discord.Embed(title="Instagram Information", description=f"**Username:** {name}\n**Followers** {followers}\n**Posts:** {posts}\n```{bio}```", color=Customize.color)
                await ctx.send(embed=embed)

    @commands.command(name="subreddit")
    async def subreddit(self, ctx, song: str):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.popcat.xyz/subreddit/{song}") as r:
                data = await r.json()
                name = data['name']
                title = data['title']
                members = data['members']
                bio = data['description']
                embed=discord.Embed(title="SubReddit Information", description=f"**Name:** {name}\n**Title** {title}\n**Members:** {members}\n```{bio}```", color=Customize.color)
                await ctx.send(embed=embed)

    @commands.command(name="steam")
    async def steam(self, ctx, song: str):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.popcat.xyz/steam?q={song}") as r:
                data = await r.json()
                name = data['name']
                type = data['type']
                price = data['price']
                bio = data['description']
                embed=discord.Embed(title="Steam Information", description=f"**Name:** {name}\n**Type** {type}\n**Price:** {price}\n```{bio}```", color=Customize.color)
                await ctx.send(embed=embed)


    @commands.command(name="hex")
    async def hex(self, ctx, song: str):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.popcat.xyz/color/{song}") as r:
                data = await r.json()
                name = data['name']
                rgb = data['rgb']
                bright = data['brightened']
                embed=discord.Embed(title="Hex Information", description=f"**Name:** {name}\n**RGB:** {rgb}\n**Brightened:** {bright}", color=Customize.color)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))