import logging
import os
import discord
from discord.ext import commands

class CustomContext(commands.Context):
    async def send(self, *args, **kwargs):
        webhook = discord.utils.get(await self.channel.webhooks(), name='Azurite Reskin')
        if webhook:
            return await webhook.send(*args, **kwargs, wait=True, username=f'{self.author.name} bot',avatar_url=self.author.display_avatar.url)
        else:
            return await super().send(*args, **kwargs)
    async def edit(self, *args, **kwargs):
        if self.message.webhook_id:
            webhook = discord.utils.get(await self.channel.webhooks(), id=self.message.webhook_id)
            return await webhook.edit_message(message_id=self.message.id, *args, **kwargs)
        else:
            return await super().edit(*args, **kwargs)

class Base(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    async def get_context(self, message, *, cls = CustomContext):
        return await super().get_context(message, cls = cls)