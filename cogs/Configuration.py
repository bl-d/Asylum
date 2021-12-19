import discord
import traceback
import sys
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import has_permissions

from utils.utils import DataBase
from utils.botcache import BotCache
from utils.utils import Methods
from utils.utils import Customize

modules = [
    'antiban',
    'antikick'
]

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, name="goodbye", help="Shows welcome commands", usage="feautres")
    @DataBase.blacklist_check()
    @commands.has_permissions()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def goodbye(self,ctx):
        embed = discord.Embed(title="Welcome", description='Sends a message when a user joins the server',color=Customize.color)
        embed.add_field(name="Commands", value="goodbye config - Sends the goodbye configuration\ngoodbye embedmessage - Sets the welcome embed message\ngoodbye embedtitle - Sets the welcome embed title\ngoodbye message - Sets the goodbye message\ngoodbye embedcolor - Sets the embed color\ngoodbye variables - Sends the goodbye variables\ngoodbye channel - Sets the goodbye channel\ngoodbye disable - Disables the goodbye module\ngoodbye enable - Enables the goodbye module\ngoodbye embeddisable - Disable the welcome embeds\ngoodbye embedenable - Enable the welcome embeds\ngoodbye test - Test the welcome command", inline=False)
        await ctx.send(embed=embed)

    @goodbye.command(name="message",help='Sets the goodbye message')
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def Goodbye_message(self,ctx,*,message):
        DataBase.db5.update_one({"guild_id": ctx.guild.id}, {"$set": {"goodbye_message": message}})
        GoodbyeMessage = DataBase.db5.find_one({"guild_id": ctx.guild.id})["goodbye_message"]
        BotCache.goodbyemessage[f'{ctx.guild.id}'] = GoodbyeMessage
        return await ctx.send(embed=discord.Embed(description=f"Successfully **set** the goodbye message {BotCache.goodbyemessage.get(f'{ctx.guild.id}')}", color=Customize.color))

    @goodbye.command(name="variables",help='Sends the goodbye variables')  
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def Goodbye_variables(self, ctx):
        return await ctx.send(embed=discord.Embed(title='Goodbye Variables',description="{user.id}\n{user.mention}\n{user.name}\n{user.tag}\n{server.name}\n{server.icon}\n{server.membercount}", color=Customize.color))
 
    @goodbye.command(name="channel",help='Sets the goodbye channel')       
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def Goodbye_channel(self, ctx, channel : discord.TextChannel):
        DataBase.db5.update_one({"guild_id": ctx.guild.id}, {"$set": {"goodbye_channel": channel.id}})
        GoodbyeChannel = DataBase.db5.find_one({"guild_id": ctx.guild.id})["goodbye_channel"]
        BotCache.goodbyechannel[f'{ctx.guild.id}'] = GoodbyeChannel
        return await ctx.send(embed=discord.Embed(description="Successfully **set** the goodbye channel", color=Customize.color))



    @goodbye.command(name="disable",help='Disables the goodbye module')  
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def Goodbye_disable(self, ctx):
        DataBase.db5.update_one({"guild_id": ctx.guild.id}, {"$set": {"goodbye_toggle": "Disabled"}})
        GoodbyeToggle = DataBase.db5.find_one({"guild_id": ctx.guild.id})["goodbye_toggle"]
        BotCache.goodbyetoggle[f'{ctx.guild.id}'] = f'{GoodbyeToggle}'
        return await ctx.send(embed=discord.Embed(description="Successfully **disabled** the goodbye module", color=Customize.color))

    @goodbye.command(name="enable",help='Enables the goodbye module')  
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def Goodbye_enable(self, ctx):
        DataBase.db5.update_one({"guild_id": ctx.guild.id}, {"$set": {"goodbye_toggle": "Enabled"}})
        GoodbyeToggle = DataBase.db5.find_one({"guild_id": ctx.guild.id})["goodbye_toggle"]
        BotCache.goodbyetoggle[f'{ctx.guild.id}'] = f'{GoodbyeToggle}'
        return await ctx.send(embed=discord.Embed(description="Successfully **enabled** the goodbye module", color=Customize.color))

    @goodbye.command(name="embedenable",help='Enable the welcome embeds')  
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def goodbye_embedenable(self, ctx):
        DataBase.db5.update_one({"guild_id": ctx.guild.id}, {"$set": {"goodbye_embed_toggle": "Enabled"}})
        return await ctx.send(embed=discord.Embed(description="Successfully **enabled** the goodbye embed module", color=Customize.color))

    @goodbye.command(name="embeddisable",help='Disable the welcome embeds')       
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def goodbye_embeddisable(self, ctx):
        DataBase.db5.update_one({"guild_id": ctx.guild.id}, {"$set": {"goodbye_embed_toggle": "Disabled"}})
        return await ctx.send(embed=discord.Embed(description="Successfully **disabled** the goodbye embed module", color=Customize.color))

    @goodbye.command(name="embedcolor",help='Sets the embed color')       
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def goodbye_embedcolor(self, ctx, color):
        DataBase.db5.update_one({"guild_id": ctx.guild.id}, {"$set": {"goodbye_color": color}})
        return await ctx.send(embed=discord.Embed(description="Successfully **set** the goodbye embed color", color=Customize.color))

    @goodbye.command(name="embedmessage",help='Sets the welcome embed emssage')
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def goodbye_embedmessage(self,ctx,*,message):
        DataBase.db5.update_one({"guild_id": ctx.guild.id}, {"$set": {"goodbye_message": message}})
        return await ctx.send(embed=discord.Embed(description="Successfully **set** the goodbye embed message", color=Customize.color))

    @goodbye.command(name="embedtitle",help='Sets the welcome embed emssage')
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def goodbye_embedtitle(self,ctx,*,message):
        DataBase.db5.update_one({"guild_id": ctx.guild.id}, {"$set": {"goodbye_embed_title": message}})
        return await ctx.send(embed=discord.Embed(description="Successfully **set** the goodbye embed title", color=Customize.color))

    @goodbye.command(name="config",help='Sends the goodbye configuration', pass_context=True)  
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def Goodbye_configuration(self, ctx):
        WelcomeToggleFind = DataBase.db5.find_one({"guild_id": ctx.guild.id})['goodbye_toggle']
        WelcomeEmbedToggleFind = DataBase.db5.find_one({"guild_id": ctx.guild.id})['goodbye_embed_toggle']
        WelcomeChannelFind = DataBase.db5.find_one({"guild_id": ctx.guild.id})['goodbye_channel']
        WelcomeEmbedColor = DataBase.db5.find_one({"guild_id": ctx.guild.id})['goodbye_embed_color']



        if WelcomeChannelFind == None:
            channel = '`None Selected`'
        else:
            channel = f'<#{WelcomeChannelFind}>'

        if WelcomeToggleFind == 'Disabled':
            wtoggle = 'Disabled'
        else:
            wtoggle = 'Enabled'

        if WelcomeEmbedToggleFind == 'Disabled':
            wetoggle = 'Disabled'
        else:
            wetoggle = 'Enabled'

        return await ctx.send(embed=discord.Embed(title='Goodbye Config',description=f"Goodbye Status: `{wtoggle}`\nGoodbye Embed Status: `{wetoggle}`\nGoodbye Embed Color: `#{WelcomeEmbedColor}`\nChannel: {channel}", color=Customize.color))

    @goodbye.command(name='test',help='Test the welcome command')     
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def goodbye_test(self, ctx):
        try:
            guild = ctx.guild
            user = ctx.author
            goodbyetoggle1 = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_toggle']
            goodbyetoggle2 = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_embed_toggle']
            channel1 = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_channel']
            message = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_message']

            if goodbyetoggle2 == 'Enabled':
                
                channel = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_channel']
                message = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_message']
                title = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_embed_title']
                colorr = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_embed_color']
                color = int(colorr, 0)
                if title == None:
                    title = 'No title selected'
                if message == None:
                    message = 'No message selected'

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
                    channelsend = self.bot.get_channel(channel)
                    await channelsend.send(embed=embed)
                    await ctx.send(embed=discord.Embed(description="Successfully **tested** the goodbye message", color=Customize.color))
                    return
        
                if message == None:
                    embed=discord.Embed(title=f"{title}", color=color)
                    channelsend = self.bot.get_channel(channel)
                    await channelsend.send(embed=embed)
                    await ctx.send(embed=discord.Embed(description="Successfully **tested** the goodbye message", color=Customize.color))
                    return

                if message and title == None:
                    channelsend = self.bot.get_channel(channel)
                    await channelsend.send(message)
                    await ctx.send(embed=discord.Embed(description="Successfully **tested** the goodbye message", color=Customize.color))
                    return

                embed=discord.Embed(title=f'{title}', description=f"{message}", color=color)
                channelsend = self.bot.get_channel(channel)
                await channelsend.send(embed=embed)
                await ctx.send(embed=discord.Embed(description="Successfully **tested** the goodbye message", color=Customize.color))
                return


            if goodbyetoggle1 == 'Enabled':
                message = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_message']
                title = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_embed_title']
                colorr = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_embed_color']
                color = int(colorr, 0)
                if title == None:
                    title = 'No title selected'
                if message == None:
                    message = 'No message selected'

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
                channel1 = DataBase.db5.find_one({"guild_id": guild.id})['goodbye_channel']
                channelsend = self.bot.get_channel(channel1)
                await channelsend.send(message)
                await ctx.send(embed=discord.Embed(description="Successfully **tested** the goodbye message", color=Customize.color))
                return

            
        except Exception:
            print(traceback.format_exc())
            print(sys.exc_info()[2])

    @commands.group(invoke_without_command=True, name="autorole", help="Shows welcome commands")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def autorole(self, ctx):
        embed = discord.Embed(title="Autorole",description='Gives a role to a user when they join the server', color=Customize.color)
        embed.add_field(name="Commands", value="autorole add - Adds a role to the autorole list\nautorole remove - Removes a role from the autorole list\nautorole disable - Disables the autorole module\nautorole enable - Enables the autorole module\nautorole config - Shows the autorole module configuration", inline=False)
        await ctx.send(embed=embed)

    @autorole.command(name="add",help='Adds a rle to the autorole list')
    @commands.has_permissions(manage_roles=True)
    async def autorole_add(self, ctx, role: discord.Role):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$push": {"autoroles": role.id}})
        embed = discord.Embed(description=f"Successfully **added** {role.mention} to the autorole list", color=Customize.color)
        await ctx.send(embed=embed)

    @autorole.command(name="remove",help='Removs a selected role')
    @has_permissions(manage_roles=True)
    async def autorole_remove(self, ctx, role: discord.Role):
            data = DataBase.db3.find_one({"guild": ctx.guild.id})
            AutoRoles = DataBase.db3.find_one({ "guild_id": ctx.guild.id })['autoroles']
        

            if role.id not in AutoRoles:
                embed1 = discord.Embed(description=f"{role.mention} is not a **selected** autorole", color=Customize.color)
                return await ctx.send(embed=embed1)
            
            DataBase.db3.update_one({"guild_id": ctx.guild.id}, { "$pull": { "autoroles": role.id }})
            embed= discord.Embed(description=f"Successfully **removed** {role.mention} from the autorole list", color=Customize.color)
            await ctx.send(embed=embed)


    @autorole.command(name="disable",help='Disables the autorole module')
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def autorole_disable(self, ctx):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$set": {"autorole_toggle": "Disabled"}})
        return await ctx.send(embed=discord.Embed(description="Successfully **disabled** the auto-role module", color=Customize.color))

    @autorole.command(name="enable",help='Enables the autorole module')
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def enable(self, ctx):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$set": {"autorole_toggle": "Enabled"}})
        return await ctx.send(embed = discord.Embed(description=f"Successfully **enabled** the auto-role module", color=Customize.color))

    @autorole.command(name="config",help='Sends the autorole configuration')
    @commands.cooldown(3, 14, BucketType.user)
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_roles=True)
    async def autorole_configurationNf(self, ctx):
        try:
            AutoRoleToggle = DataBase.db3.find_one({"guild_id": ctx.guild.id})['autorole_toggle']
            

            if AutoRoleToggle == 'Disabled':
                atoggle = 'Disabled'
            else:
                atoggle = 'Enabled'
            data = DataBase.db3.find_one({"guild_id": ctx.guild.id})
            for roleID in data['autoroles']:
                role = ctx.guild.get_role(roleID)
        
            return await ctx.send(embed = discord.Embed(title=f"Autorole Config", color=Customize.color, description = f'Status: `{atoggle}`\nRoles: {role.mention}'))
        except:
            return await ctx.send(embed = discord.Embed(title=f"Autorole Config Error", color=Customize.color, description = f'Before you can run this command, you must add a autorole, do this by running `.autorole add [role]`'))

    @commands.group(invoke_without_command=True, name="welcome", help="Shows welcome commands")
    @DataBase.blacklist_check()
    @commands.has_permissions()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome(self,ctx):
        embed = discord.Embed(title="Welcome", description='Sends a message when a user joins the server',color=Customize.color)
        embed.add_field(name="Commands", value="welcome embedmessage - Sets the welcome embed message\nwelcome embedtitle - Sets the welcome embed title\nwelcome message - Sets the welcome message\nwelcome test - Test the welcome command\nwelcome variables - Sends the welcome variables\nwelcome config - Sends the welcome configuration\nwelcome channel - Set the welcome channel\nwelcome disable - Disable the welcome module\nwelcome embedcolor - Sets the embed color\nwelcome enable - Enable the welcome module\nwelcome embeddisable - Disable the welcome embeds\nwelcome embedenable - Enable the welcome embeds", inline=False)
        await ctx.send(embed=embed)

    @welcome.command(name="message",help='Sets the welcome emssage')
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_message(self,ctx,*,message):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$set": {"welcome_message": message}})
        WelcomeMessage = DataBase.db3.find_one({"guild_id": ctx.guild.id})["welcome_message"]
        BotCache.welcomemessage[f'{ctx.guild.id}'] = WelcomeMessage

        return await ctx.send(embed=discord.Embed(description="Successfully **set** the welcome message", color=Customize.color))

    @welcome.command(name="variables",help='Sends the welcome variables')      
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_variables(self, ctx):
        return await ctx.send(embed=discord.Embed(title='Welcome Variables',description="{user.id}\n{user.mention}\n{user.name}\n{user.tag}\n{server.name}\n{server.icon}\n{server.membercount}", color=Customize.color))
 
    @welcome.command(name="config",help='Sends the welcome configuration')     
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_configurationN(self, ctx):
        WelcomeToggleFind = DataBase.db3.find_one({"guild_id": ctx.guild.id})['welcome_toggle']
        WelcomeEmbedToggleFind = DataBase.db3.find_one({"guild_id": ctx.guild.id})['welcome_embed_toggle']
        WelcomeChannelFind = DataBase.db3.find_one({"guild_id": ctx.guild.id})['welcome_channel']
        WelcomeEmbedColor = DataBase.db3.find_one({"guild_id": ctx.guild.id})['welcome_embed_color']



        if WelcomeChannelFind == None:
            channel = '`None Selected`'
        else:
            channel = f'<#{WelcomeChannelFind}>'

        if WelcomeToggleFind == 'Disabled':
            wtoggle = 'Disabled'
        else:
            wtoggle = 'Enabled'

        if WelcomeEmbedToggleFind == 'Disabled':
            wetoggle = 'Disabled'
        else:
            wetoggle = 'Enabled'

        return await ctx.send(embed=discord.Embed(title='Welcome Config',description=f"Welcome Status: `{wtoggle}`\nWelcome Embed Status: `{wetoggle}`\nWelcome Embed Color: `#{WelcomeEmbedColor}`\nChannel: {channel}", color=Customize.color))

    @welcome.command(name="channel",help='Set the welcome channel')       
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_channel(self, ctx, channel : discord.TextChannel):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$set": {"welcome_channel": channel.id}})
        WelcomeChannel = DataBase.db3.find_one({"guild_id": ctx.guild.id})["welcome_channel"]
        BotCache.welcomechannel[f'{ctx.guild.id}'] = WelcomeChannel
        return await ctx.send(embed=discord.Embed(description="Successfully **set** the welcome channel", color=Customize.color))
    

    @welcome.command(name="disable",help='Disable the welcome module')       
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_disable(self, ctx):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$set": {"welcome_toggle": "Disabled"}})
        return await ctx.send(embed=discord.Embed(description="Successfully **disabled** the welcome module", color=Customize.color))

    @welcome.command(name="enable",help='Enable the welcome module')    
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_enable(self, ctx):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$set": {"welcome_toggle": "Enabled"}})
        WelcomeToggle = DataBase.db3.find_one({"guild_id": ctx.guild.id})["welcome_toggle"]
        BotCache.welcometoggle[f'{ctx.guild.id}'] = f'{WelcomeToggle}'
        return await ctx.send(embed=discord.Embed(description="Successfully **enabled** the welcome module", color=Customize.color))
#-------------------------------------------------------------------------------------------------------------------------------------------------------

    @welcome.command(name="embedenable",help='Enable the welcome embeds')  
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_embedenable(self, ctx):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$set": {"welcome_embed_toggle": "Enabled"}})
        return await ctx.send(embed=discord.Embed(description="Successfully **enabled** the welcome embed module", color=Customize.color))

    @welcome.command(name="embeddisable",help='Disable the welcome embeds')       
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_embeddisable(self, ctx):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$set": {"welcome_embed_toggle": "Disabled"}})
        return await ctx.send(embed=discord.Embed(description="Successfully **disabled** the welcome embed module", color=Customize.color))

    @welcome.command(name="embedcolor",help='Sets the embed color')       
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_embedcolor(self, ctx, color):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$set": {"welcome_embed_color": color}})
        return await ctx.send(embed=discord.Embed(description="Successfully **set** the welcome embed color", color=Customize.color))

    @welcome.command(name="embedmessage",help='Sets the welcome embed emssage')
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_embedmessage(self,ctx,*,message):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$set": {"welcome_embed_message": message}})
        return await ctx.send(embed=discord.Embed(description="Successfully **set** the welcome embed message", color=Customize.color))

    @welcome.command(name="embedtitle",help='Sets the welcome embed emssage')
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_embedtitle(self,ctx,*,message):
        DataBase.db3.update_one({"guild_id": ctx.guild.id}, {"$set": {"welcome_embed_title": message}})
        return await ctx.send(embed=discord.Embed(description="Successfully **set** the welcome embed title", color=Customize.color))

#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #user = ctx.author
    @welcome.command(name='test',help='Test the welcome command')     
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_test(self, ctx):
        try:
            guild = ctx.guild
            user = ctx.author
            goodbyetoggle1 = DataBase.db3.find_one({"guild_id": guild.id})['welcome_toggle']
            goodbyetoggle2 = DataBase.db3.find_one({"guild_id": guild.id})['welcome_embed_toggle']
            channel1 = DataBase.db3.find_one({"guild_id": guild.id})['welcome_channel']
            message = DataBase.db3.find_one({"guild_id": guild.id})['welcome_message']

            if goodbyetoggle2 == 'Enabled':
                
                channel = DataBase.db3.find_one({"guild_id": guild.id})['welcome_channel']
                message = DataBase.db3.find_one({"guild_id": guild.id})['welcome_message']
                title = DataBase.db3.find_one({"guild_id": guild.id})['welcome_embed_title']
                colorr = DataBase.db3.find_one({"guild_id": guild.id})['welcome_embed_color']
                color = int(colorr, 0)
                if title == None:
                    title = 'No title selected'
                if message == None:
                    message = 'No message selected'

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
                    channelsend = self.bot.get_channel(channel)
                    await channelsend.send(embed=embed)
                    await ctx.send(embed=discord.Embed(description="Successfully **tested** the welcome message", color=Customize.color))
                    return
        
                if message == None:
                    embed=discord.Embed(title=f"{title}", color=color)
                    channelsend = self.bot.get_channel(channel)
                    await channelsend.send(embed=embed)
                    await ctx.send(embed=discord.Embed(description="Successfully **tested** the welcome message", color=Customize.color))
                    return

                if message and title == None:
                    channelsend = self.bot.get_channel(channel)
                    await channelsend.send(message)
                    await ctx.send(embed=discord.Embed(description="Successfully **tested** the welcome message", color=Customize.color))
                    return

                embed=discord.Embed(title=f'{title}', description=f"{message}", color=color)
                channelsend = self.bot.get_channel(channel)
                await channelsend.send(embed=embed)
                await ctx.send(embed=discord.Embed(description="Successfully **tested** the welcome message", color=Customize.color))
                return


            if goodbyetoggle1 == 'Enabled':
                message = DataBase.db3.find_one({"guild_id": guild.id})['welcome_message']
                title = DataBase.db3.find_one({"guild_id": guild.id})['welcome_embed_title']
                colorr = DataBase.db3.find_one({"guild_id": guild.id})['welcome_embed_color']
                color = int(colorr, 0)
                if title == None:
                    title = 'No title selected'
                if message == None:
                    message = 'No message selected'

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
                channel1 = DataBase.db3.find_one({"guild_id": guild.id})['welcome_channel']
                channelsend = self.bot.get_channel(channel1)
                await channelsend.send(message)
                await ctx.send(embed=discord.Embed(description="Successfully **tested** the welcome message", color=Customize.color))
                return

            
        except Exception:
            print(traceback.format_exc())
            # or
            print(sys.exc_info()[2])

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def prefix(self, ctx, prefix: str):
        DataBase.db1.update_one({"guild_id": ctx.guild.id}, {"$set": {"prefix": prefix}})
        prefixx = DataBase.db1.find_one({"guild_id": ctx.guild.id})["prefix"]
        BotCache.prefixes[f'{ctx.guild.id}'] = f'{prefixx}'
        embed = discord.Embed(description=f"Successfully **updated** the prefix to `{prefix}`\n", color=Customize.color)
        await ctx.send(embed=embed)

# -------------------------------------------------------------------------------------------------------------------------
# Settings Cmds

    @commands.group(invoke_without_command=True, name="settings", help="Shows Asylums settings")
    @DataBase.blacklist_check()
    @commands.has_permissions()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def settings(self,ctx):
        embed = discord.Embed(title="Asylum's Settings", description='These set of commands can show quickly show you the generic basic settings of are modules. If you want to know how to switch somthing, or check the status these are the commands for you.',color=Customize.color)
        embed.add_field(name="Commands", value="settings overall - Shows the overale configuration\nsettings welcome - Shows the welcome module settings\nsettings goodbye - Shows the goodbye module settings\nsettings autorole - Shows the autorole module settings", inline=False)
        await ctx.send(embed=embed)

# -------------------------------------------------------------------------------------------------------------------------



    @commands.group(invoke_without_command=True, name="antinuke", help="Shows antinuke commands", usage="feautres")
    @DataBase.blacklist_check()
    @commands.has_permissions()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def antinuke(self,ctx):
        embed = discord.Embed(title="Antinuke", description='Protects your server from malicious attacks',color=Customize.color)
        embed.add_field(name="Commands", value="coming soon", inline=False)
        await ctx.send(embed=embed)



    @antinuke.command(name="toggle",help='Toggles said module')
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def antinuke_toggle(self, ctx, module = None, toggle = None):
        if module == None:
            return await ctx.send(embed=discord.Embed(title='Toggle Error',description=f"Please **select** a module to toggle", color=Customize.color))

        if module not in modules:
            return await ctx.send(embed=discord.Embed(title='Toggle Error',description=f"Please **select** a  proper module to toggle", color=Customize.color))

        if module in modules:
            if toggle == None:
                return await ctx.send(embed=discord.Embed(title='Toggle Error',description=f"Please select if you would like to enable or disable the **module**", color=Customize.color))

            if toggle == 'on':
                DataBase.db6.update_one({"guild_id": ctx.guild.id}, {"$set": {"antiban_toggle": True}})
                return await ctx.send(embed=discord.Embed(title='Toggle Success',description=f"Successfully enabled the **{module}** module", color=Customize.color))

            if toggle == 'off':
                DataBase.db6.update_one({"guild_id": ctx.guild.id}, {"$set": {"antiban_toggle": False}})
                return await ctx.send(embed=discord.Embed(title='Toggle Success',description=f"Successfully disabled the **{module}** module", color=Customize.color))




    @antinuke.command(name="overview",help='Sends the goodbye configuration', pass_context=True)  
    @DataBase.blacklist_check()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def antinuke_ovwerview(self, ctx):
        AntibanToggleFind = DataBase.db6.find_one({"guild_id": ctx.guild.id})['antiban_toggle']
        AntikickToggleFind = DataBase.db6.find_one({"guild_id": ctx.guild.id})['antikick_toggle']

        AntichannelcreateToggleFind = DataBase.db6.find_one({"guild_id": ctx.guild.id})['antiban_toggle']
        AntichannelcreateToggleFind = DataBase.db6.find_one({"guild_id": ctx.guild.id})['antiban_toggle']

        AntirolecreateToggleFind = DataBase.db6.find_one({"guild_id": ctx.guild.id})['antiban_toggle']
        AntiroledeleteToggleFind = DataBase.db6.find_one({"guild_id": ctx.guild.id})['antiban_toggle']




        if AntibanToggleFind == True:
            bantoggle = '<:Approve:907817002977095691>'
        else:
            bantoggle = f'<:Deny:907816979824508979>'
        if AntikickToggleFind == True:
            kicktoggle = '<:Approve:907817002977095691>'
        else:
            kicktoggle = f'<:Deny:907816979824508979>'
        if AntichannelcreateToggleFind == True:
            channelcreatetoggle = '<:Approve:907817002977095691>'
        else:
            channelcreatetoggle = f'<:Deny:907816979824508979>'
        if AntikickToggleFind == True:
            kicktoggle = '<:Approve:907817002977095691>'
        else:
            kicktoggle = f'<:Deny:907816979824508979>'

        return await ctx.send(embed=discord.Embed(title='Antinuke Overview',description=f"**Antiban:** {bantoggle}\n**kick:** {kicktoggle}\nAnti Channel Create", color=Customize.color))


def setup(bot):
    bot.add_cog(Configuration(bot))
