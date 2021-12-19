import discord
from discord.ext import commands

from utils.paginator import *
from utils.utils import Customize

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.tasks = []

    @commands.command(name="nuke")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        channel = channel if channel else ctx.channel
        newchannel = await channel.clone()
        await newchannel.edit(position=channel.position)
        await channel.delete()
        embed = discord.Embed(title="Nuke Success", description=F"Channel has been nuked by {ctx.author}", color=Customize.color)
        await newchannel.send(embed=embed, delete_after=5)

    @commands.command(name="ban")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.guild.owner.id != ctx.author.id:
            if member.top_role >= ctx.author.top_role:
                return await ctx.send(embed=discord.Embed(title="Ban Error", description=f"`{member.name}`'s role is higher than yours\nYou cant ban someone with a higher role", color=Customize.color))
        if ctx.guild.owner == member:
                return await ctx.send(embed=discord.Embed(title="Ban Error", description=f"`{member.name}` is the owner of the server\nI cannot ban the owner", color=Customize.color))
        if ctx.author == member:
            return await ctx.send(embed=discord.Embed(title="Ban Error", description=f"`{member.name}`is yourself\nYou cannot ban yourself", color=Customize.color))
        if member == None:
            return await ctx.send(embed=discord.Embed(title="Ban Error", description=f"No member has been selected\nPlease select a member", color=Customize.color))
        await member.kick(reason=reason)
        await ctx.send(embed=discord.Embed(title="Ban Success", description=f"Successfully banned `{member.name}`\nReason: `{reason}`", color=Customize.color))

    @commands.command(name="unban")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user):
        try:
            await ctx.guild.unban(discord.Object(id=user))
            await ctx.send(embed=discord.Embed(title="Unban Success", description=f"Successfully unbanned `{user}`", color=Customize.color))
        except Exception:
            await ctx.send(embed=discord.Embed(title="Unban Error", description=f"Failed to unban `{user}`", color=Customize.color))

    @commands.command(name="purge")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(embed=discord.Embed(title="Purge Success", description=f"Successfully purged `{amount}` messages", color=Customize.color), delete_after=3)

    @commands.command(name="kick")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.guild.owner.id != ctx.author.id:
            if member.top_role >= ctx.author.top_role:
                return await ctx.send(embed=discord.Embed(title="Kick Error", description=f"`{member.name}`'s role is higher than yours\nYou cannot kick someone with a higher role", color=Customize.color))
        if ctx.guild.owner == member:
                return await ctx.send(embed=discord.Embed(title="Kick Error", description=f"`{member.name}` is the owner of the server\nI cannot kick the owner", color=Customize.color))
        if ctx.author == member:
            return await ctx.send(embed=discord.Embed(title="Kick Error", description=f"`{member.name}`is yourself\nYou cannot kick yourself", color=Customize.color))
        if member == None:
            return await ctx.send(embed=discord.Embed(title="Kick Error", description=f"No member has been selected\nPlease select a member", color=Customize.color))
        await member.kick(reason=reason)
        await ctx.send(embed=discord.Embed(title="Kick Success", description=f"Successfully kicked `{member.name}`\nReason: `{reason}`", color=Customize.color))

    @commands.command(name="slowmode")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds: int=0):
        if seconds > 120:
            return await ctx.send(embed=discord.Embed(title="Slowmode Error", description="Slowmode cannot be over 2 minutes", color=Customize.color))
        if seconds == 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(embed=discord.Embed(title="Slowmode Success", description="Slowmode is disabled", color=Customize.color))
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(embed=discord.Embed(title="Slowmode Success", description=f"Set slowmode to `{seconds}`", color=Customize.color))

    @commands.command(name="unslowmode")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def unslowmode(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send(embed=discord.Embed(title="Unslowmode Success", description="Disabled slowmode", color=Customize.color))

    @commands.command(name="roleall")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def role_all(self, ctx, *, role: discord.Role):
        if ctx.guild.id in self.tasks:
            return await ctx.send(embed=discord.Embed(title="Roleall", description="There is a roleall task already running, please wait for it to finish", color=Customize.color))
        await ctx.message.add_reaction('<:AsylumCorrect:891704856660832266>')
        num = 0
        failed = 0
        for user in list(ctx.guild.members):
            try:
                await user.add_roles(role)
                num += 1
            except Exception:
                failed += 1
        await ctx.send(embed=discord.Embed(title="Roleall", description="Successfully added **`%s`** to **`%s`** users, failed to add it to **`%s`** users" % (role.name, num, failed), color=Customize.color))


    @commands.command(name="cleanup")
    @commands.has_permissions(administrator=True)
    async def cleanup(self, ctx, amount: int):
        msg = await ctx.send("cleaning up my messages")
        async for message in ctx.message.channel.history(limit=amount).filter(lambda m: m.author == self.bot.user).map(lambda m: m):
            try:
                if message.id == msg.id:
                    pass
                else:
                    await message.delete()
            except:
                pass
        await msg.edit(content="cleaned up my messages 👍")

    @commands.command(name="jail")
    @commands.has_permissions(administrator=True)
    async def jail(self, ctx, member: discord.Member, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="jailed")
        if not role:
            await ctx.guild.create_role(name="jailed")

        jail = discord.utils.get(ctx.guild.text_channels, name="jail")
        if not jail:
            try:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
                }            
                jail = await ctx.guild.create_text_channel("jail", overwrites=overwrites)
                await ctx.send(embed=discord.Embed(title="Jail Setup", description="I could not find a proper jail channel for this server.\nI have created one: %s" % (jail.mention), color=Customize.color))
            except discord.Forbidden:
                return await ctx.send(embed=discord.Embed(title="Jail Setup", description="I do not have the proper permissions to setup the Jail function", color=Customize.color))

        for channel in ctx.guild.channels:
            if channel.name == "jail":
                perms = channel.overwrites_for(member)
                perms.send_messages = True
                perms.read_messages = True
                await channel.set_permissions(member, overwrite=perms)
            else:
                perms = channel.overwrites_for(member)
                perms.send_messages = False
                perms.read_messages = False
                perms.view_channel = False
                await channel.set_permissions(member, overwrite=perms)

        role = discord.utils.get(ctx.guild.roles, name="jailed")
        await member.add_roles(role)

        await jail.send(content=member.mention, embed=discord.Embed(title="Jailed User", description=f"You have been jailed by a moderator.\nReason: `{reason}`\nPlease contact them for further information.", color=Customize.color))
        await ctx.send(embed=discord.Embed(title="Jailed User", description=f"Successfully jailed {member.mention}\nReason: `{reason}`", color=Customize.color))

    @commands.command(name="unjail")
    @commands.has_permissions(administrator=True)
    async def unjail(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="jailed")
        for channel in ctx.guild.channels:
            if channel.name == "jail":
                perms = channel.overwrites_for(member)
                perms.send_messages = None
                perms.read_messages = None
                await channel.set_permissions(member, overwrite=perms)
            else:
                perms = channel.overwrites_for(member)
                perms.send_messages = None
                perms.read_messages = None
                perms.view_channel = None
                await channel.set_permissions(member, overwrite=perms)

        await ctx.send(embed=discord.Embed(title="Unjailed User", description="I have successfully unjailed **`%s`**" % (member.name), color=Customize.color))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, userid, *, reason=None):
            try:
                userid = int(userid)
            except:
                await ctx.send('Invalid ID')
                return
        
            try:
                await ctx.guild.ban(discord.Object(userid), reason=reason)
                await ctx.send(embed=discord.Embed(title="Ban Success", description=f"Successfully banned `{userid}`\nReason: `{reason}`", color=Customize.color))
            except Exception as e:
                return await ctx.send(embed=discord.Embed(title="Hackban Error", description=f"I could not ban `{userid}`", color=Customize.color))

    @commands.command(
        name="lock",
        description="Locks down a channel.",
        usage="lock `#<channel>` [reason]",
    )
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def lock(self, ctx, channel:discord.TextChannel = None, *, reason=None):

            if channel is None: channel = ctx.channel
            try:
                await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
                await ctx.send(embed=discord.Embed(title="Lock Success", description=f"Successfully locked `#{channel}`\nReason: `{reason}`", color=Customize.color))
            except:
                return await ctx.send(embed=discord.Embed(title="Lock Error", description=f"I could not lock `#{channel}`", color=Customize.color))
            else:
                pass

    @commands.command(
        name="unlock",
        description="Unlocks a channel.",
        usage="unlock `#<channel>`",
    )
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def unlock(self, ctx, channel:discord.TextChannel = None, *, reason=None):
            if channel is None: channel = ctx.channel
            try:
                await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = True), reason=reason)
                await ctx.send(embed=discord.Embed(title="Unlock Success", description=f"Successfully unlocked `#{channel}`\nReason: `{reason}`", color=Customize.color))
            except:
                return await ctx.send(embed=discord.Embed(title="Unlock Error", description=f"I could not unlock `#{channel}`", color=Customize.color))
            else:
                pass

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def lockall(self, ctx, server:discord.Guild = None, *, reason=None):
            if server is None: server = ctx.guild
            try:
                for channel in server.channels:
                    await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
                await ctx.send(embed=discord.Embed(title="Lock Success", description=f"Successfully locked down `{server}`\nReason: `{reason}`", color=Customize.color))
            except:
                return await ctx.send(embed=discord.Embed(title="Lock Error", description=f"I could not lock down `{server}`", color=Customize.color))
            else:
                pass

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def unlockall(self, ctx, server:discord.Guild = None, *, reason=None):
            if server is None: server = ctx.guild
            try:
                for channel in server.channels:
                    await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = True), reason=reason)
                await ctx.send(embed=discord.Embed(title="Unlock Success", description=f"Successfully unlocked `{server}`\nReason: `{reason}`", color=Customize.color))
            except:
                return await ctx.send(embed=discord.Embed(title="Lock Error", description=f"I could not unlock `{server}`", color=Customize.color))
            else:
                pass



    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(2, 5, commands.BucketType.channel)
    async def mute(self, ctx, member: discord.Member, *, reason: str = None):
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")
        perms = discord.Permissions(send_messages=False, read_messages=True)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            await ctx.guild.create_role(name="muted", permissions=perms)
        if member.top_role >= ctx.author.top_role:
            await ctx.send(embed=discord.Embed(title="Mute Error", description=f"You cannot mute a user above you", color=Customize.color))
            return
        if not muted_role:
            try:
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="Mute Success", description=f"Successfully muted `{member}`\nReason: `{reason}`", color=Customize.color))
            except:
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="Mute Success", description=f"Successfully muted `{member}`\nReason: `{reason}`", color=Customize.color))
        else:
            try:
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="Mute Success", description=f"Successfully muted `{member}`\nReason: `{reason}`", color=Customize.color))
            except:
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="Mute Success", description=f"Successfully muted `{member}`\nReason: `{reason}`", color=Customize.color))

    @commands.command(
        name="unmute",
        description="Unmutes the mentioned user.",
        usage="unmute <user> [reason]"
    )

    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = None):
            guild = ctx.guild
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if member.top_role >= ctx.author.top_role:
              await ctx.send(embed=discord.Embed(title="Unmute Error", description=f"You cannot unmute a user above you", color=Customize.color))
              return
            if not muted_role:
                await ctx.send(embed=discord.Embed(title="Unmute Error", description=f"`{member}` is not muted", color=Customize.color))
                return
            else:
                try:
                    try:

                        await member.remove_roles(muted_role)
                        await ctx.send(embed=discord.Embed(title="Unmute Success", description=f"Successfully unmuted `{member}`\nReason: `{reason}`", color=Customize.color))
                    except:
                        await member.remove_roles(muted_role)
                        await ctx.send(embed=discord.Embed(title="Unmute Success", description=f"Successfully unmuted `{member}`\nReason: `{reason}`", color=Customize.color))
                except Exception as e:
                        await ctx.send(embed=discord.Embed(title="Unmute Error", description=f"Failed to unmute `{member}`", color=Customize.color))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(2, 5, commands.BucketType.channel)
    async def rmute(self, ctx, member: discord.Member, *, reason: str = None):
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="rMuted")
        perms = discord.Permissions(add_reactions=False, use_external_emojis=False, read_messages=True)
        role = discord.utils.get(ctx.guild.roles, name="rMuted")
        if not role:
            await ctx.guild.create_role(name="rMuted", permissions=perms)
        if member.top_role >= ctx.author.top_role:
            await ctx.send(embed=discord.Embed(title="rMute Error", description=f"You cannot rMuted a user above you", color=Customize.color))
            return
        if not muted_role:
            try:
                role = discord.utils.get(ctx.guild.roles, name="rMuted")
                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="rMute Success", description=f"Successfully rMuted `{member}`\nReason: `{reason}`", color=Customize.color))
            except:
                role = discord.utils.get(ctx.guild.roles, name="rMuted")
                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="rMute Success", description=f"Successfully rMuted `{member}`\nReason: `{reason}`", color=Customize.color))
        else:
            try:
                role = discord.utils.get(ctx.guild.roles, name="rMuted")
                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="rMute Success", description=f"Successfully rMuted `{member}`\nReason: `{reason}`", color=Customize.color))
            except:
                role = discord.utils.get(ctx.guild.roles, name="rMuted")
                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="rMute Success", description=f"Successfully rMuted `{member}`\nReason: `{reason}`", color=Customize.color))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def runmute(self, ctx, member: discord.Member, *, reason: str = None):
            guild = ctx.guild
            muted_role = discord.utils.get(ctx.guild.roles, name="rMuted")
            if member.top_role >= ctx.author.top_role:
              await ctx.send(embed=discord.Embed(title="rUnmute Error", description=f"You cannot rUnmute a user above you", color=Customize.color))
              return
            if not muted_role:
                await ctx.send(embed=discord.Embed(title="rUnmute Error", description=f"`{member}` is not rMuted", color=Customize.color))
                return
            else:
                try:
                    try:
                        muted_role = discord.utils.get(ctx.guild.roles, name="rMuted")
                        await member.remove_roles(muted_role)
                        await ctx.send(embed=discord.Embed(title="rUnmute Success", description=f"Successfully rUnmuted `{member}`\nReason: `{reason}`", color=Customize.color))
                    except:
                        muted_role = discord.utils.get(ctx.guild.roles, name="rMuted")
                        await member.remove_roles(muted_role)
                        await ctx.send(embed=discord.Embed(title="rUnmute Success", description=f"Successfully rUnmuted `{member}`\nReason: `{reason}`", color=Customize.color))
                except Exception as e:
                        await ctx.send(embed=discord.Embed(title="rUnmute Error", description=f"Failed to rNnmute `{member}`", color=Customize.color))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(2, 5, commands.BucketType.channel)
    async def imute(self, ctx, member: discord.Member, *, reason: str = None):
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="imuted")
        perms = discord.Permissions(read_messages=True)
        role = discord.utils.get(ctx.guild.roles, name="imuted")
        if not role:
            await ctx.guild.create_role(name="imuted", permissions=perms)
        if member.top_role >= ctx.author.top_role:
            await ctx.send(embed=discord.Embed(title="iMute Error", description=f"You cannot iMuted a user above you", color=Customize.color))
            return
        if not muted_role:
            try:

                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="iMute Success", description=f"Successfully iMuted `{member}`\nReason: `{reason}`", color=Customize.color))
            except:

                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="iMute Success", description=f"Successfully iMuted `{member}`\nReason: `{reason}`", color=Customize.color))
        else:
            try:

                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="iMute Success", description=f"Successfully iMuted `{member}`\nReason: `{reason}`", color=Customize.color))
            except:

                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="iMute Success", description=f"Successfully iMuted `{member}`\nReason: `{reason}`", color=Customize.color))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def iunmute(self, ctx, member: discord.Member, *, reason: str = None):
            guild = ctx.guild
            muted_role = discord.utils.get(ctx.guild.roles, name="imuted")
            if member.top_role >= ctx.author.top_role:
              await ctx.send(embed=discord.Embed(title="iUnmute Error", description=f"You cannot unmute a user above you", color=Customize.color))
              return
            if not muted_role:
                await ctx.send(embed=discord.Embed(title="iUnmute Error", description=f"`{member}` is not muted", color=Customize.color))
                return
            else:
                try:
                    try:

                        await member.remove_roles(muted_role)
                        await ctx.send(embed=discord.Embed(title="iUnmute Success", description=f"Successfully unmuted `{member}`\nReason: `{reason}`", color=Customize.color))
                    except:
                        await member.remove_roles(muted_role)
                        await ctx.send(embed=discord.Embed(title="iUnmute Success", description=f"Successfully unmuted `{member}`\nReason: `{reason}`", color=Customize.color))
                except Exception as e:
                        await ctx.send(embed=discord.Embed(title="iUnmute Error", description=f"Failed to unmute `{member}`", color=Customize.color))

def setup(client):
    client.add_cog(moderation(client))
