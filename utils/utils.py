from typing import Dict
from discord.ext import commands

import discord
from io import BytesIO
import discord
from PIL import Image
import pymongo
import re
from discord.ext import commands
from utils.botcache import BotCache
import logging
from utils.database import DataBase

regex_mention = re.compile("<@(?:!|)(\d+)>")
regex_namediscrim = re.compile("(.{2,32})#(\d{4})")
regex_id = re.compile("(^\d+$)")
regex_name = re.compile("(.{2,32})")
role_mention = re.compile("<@&(\d+)>")
channel_mention = re.compile("<#(\d+)>")
client = discord.Client()

class Checks:

    def is_owner_check(ctx):
        if ctx.author.id in [831171302336757790, 905121692978921472]:
            return True
        else:
            return False

class Customize:

    color=0xffffff

class Methods:

    logging.basicConfig(
        level=logging.INFO,
        format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
        datefmt="%H:%M:%S",
    )

    def solid_color_image(color: tuple):
        buffer = BytesIO()
        image = Image.new('RGB', (80, 80), color)
        image.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    def create_embed(ctx, title=discord.Embed.Empty, description=discord.Embed.Empty, color=0xb899ff):
        embed = discord.Embed(description=description, title=title, color=color)
        return embed

    async def entry_to_code(ctx, entries):
        width = max(map(lambda t: len(t[0]), entries))
        output = ['```']
        fmt = '{0:<{width}}: {1}'
        for name, entry in entries:
            output.append(fmt.format(name, entry, width=width))
        output.append('```')
        await ctx.send('\n'.join(output))

    def escape(text: str, *, mass_mentions: bool = False, formatting: bool = False) -> str:
        if mass_mentions:
            text = text.replace("@everyone", "@\u200beveryone")
            text = text.replace("@here", "@\u200bhere")
        if formatting:
            text = discord.utils.escape_markdown(text)
        return text

    def get_text_channel(ctx, channel):
        if channel_mention.match(channel):
            channel = discord.utils.get(ctx.guild.text_channels, id=int(channel_mention.match(channel).group(1)))
        elif regex_id.match(channel):
            channel = discord.utils.get(ctx.guild.text_channels, id=int(regex_id.match(channel).group(1)))
        else:
            try:
                channel = list(filter(lambda x: x.name.lower() == channel.lower(), ctx.guild.text_channels))[0]
            except IndexError:
                try:
                    channel = \
                    list(filter(lambda x: x.name.lower().startswith(channel.lower()), ctx.guild.text_channels))[0]
                except IndexError:
                    try:
                        channel = list(filter(lambda x: channel.lower() in x.name.lower(), ctx.guild.text_channels))[0]
                    except IndexError:
                        return None
        return channel

    def get_role(ctx, role):
        if role_mention.match(role):
            role = ctx.guild.get_role(int(role_mention.match(role).group(1)))
        elif regex_id.match(role):
            role = ctx.guild.get_role(int(regex_id.match(role).group(1)))
        else:
            try:
                role = list(filter(lambda x: x.name.lower() == role.lower(), ctx.guild.roles))[0]
            except IndexError:
                try:
                    role = list(filter(lambda x: x.name.lower().startswith(role.lower()), ctx.guild.roles))[0]
                except IndexError:
                    try:
                        role = list(filter(lambda x: role.lower() in x.name.lower(), ctx.guild.roles))[0]
                    except IndexError:
                        return None
        return role

    def get_prefix(self, message) -> str:
        if message.guild:
            try:
                prefix = DataBase.db1.find_one({"guild_id": message.guild.id})["prefix"]
                BotCache.prefixes[f'{message.guild.id}'] = f'{prefix}'
                return BotCache.prefixes.get(f'{message.guild.id}')
            except (KeyError, ValueError):
                BotCache.prefixes[f'{message.guild.id}'] = f'{prefix}'
                return self.prexies[f'{message.guild.id}']

    async def entry_to_code(ctx, entries):
        width = max(map(lambda t: len(t[0]), entries))
        output = ['```']
        fmt = '{0:<{width}}: {1}'
        for name, entry in entries:
            output.append(fmt.format(name, entry, width=width))
        output.append('```')
        await ctx.send('\n'.join(output))

    @staticmethod
    async def say_permissions(ctx, member, channel):
        permissions = channel.permissions_for(member)
        entries = [(attr.replace('_', ' ').title(), val) for attr, val in permissions]
        await Methods.entry_to_code(ctx, entries)


    @classmethod
    def find_data(cls, guild: discord.Guild, value: str = None):
        if value is not None:
            return DataBase.db3.find_one({"guild_id": guild.id})[value]
        else:
            return DataBase.db3.find_one({"guild_id": guild.id})

    def solid_color_image(color: tuple):
        buffer = BytesIO()
        image = Image.new('RGB', (80, 80), color)
        image.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    def embed_create(ctx, title=discord.Embed.Empty, description=discord.Embed.Empty, color=0x46ff2e):
        embed = discord.Embed(description=description, title=title, color=color)
        return embed

    def create_embed(text):
        embed = discord.Embed(description=text,colour=0x36393F,)
        return embed



class BotCache:
    prefixes = {}
    welcometoggle = {}
    welcometoggleembed= {}
    welcomemessage = {}
    welcomechannel = {}
    goodbyetoggle = {}
    goodbyetoggleembed = {}
    goodbyemessage = {}
    goodbyechannel = {}
    autoroletoggle = {}
    autoroles = {}

    antibantoggle = {}
    antikicktoggle = {}
    antichannelcreatetoggle = {}
    antichanneldeletetoggle = {}
    antirolecreatetoggle = {}
    antiroledeletetoggle = {}

    antibanlimit = {}
    antikicklimit = {}
    antichannelcreatelimit = {}
    antichanneldeletelimit = {}
    antirolecreatelimit = {}
    antiroledeletelimit = {}
