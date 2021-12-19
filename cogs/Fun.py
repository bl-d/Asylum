import json
import random
from io import BytesIO
import aiohttp
import discord
from discord_webhook import DiscordWebhook, DiscordEmbed
import giphy_client
import pymongo
import requests
from PIL import Image
from typing import Union, Optional
from discord import Embed
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
from giphy_client.rest import ApiException

from utils.utils import Methods
from utils.help import AsylumHelp
from utils.utils import Customize
from utils.utils import DataBase

async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()



class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=1)
    async def clean_mods(self):
        await self.bot.wait_until_ready()
        if self.abusewatch != {}:
            self.abusewatch = {}

    @commands.command(help='Cuddles said user')
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def cuddle(self, ctx, member: commands.MemberConverter):
        r = requests.get(f'https://nekos.life/api/v2/img/cuddle').json()
        url = r["url"]
        embed = discord.Embed(description=f"{ctx.author.mention} cuddled {member.mention}", color=Customize.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(help='Cuddles said user')
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def cuddleo(self, ctx):
        for emoji in ctx.guild.emojis:
            await ctx.send(f'```<:{emoji.name}:{emoji.id}>```\n<:{emoji.name}:{emoji.id}>')

    @commands.command()
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            dogjson = await request.json()
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
      response = requests.get('https://aws.random.cat/meow')
      data = response.json()
      embed = discord.Embed(color=Customize.color)
      embed.set_image(url=data['file'])            
      await ctx.send(embed=embed)

    @commands.command(help='Hug said user')
    @commands.cooldown(3, 5, commands.BucketType.user)   
    async def hug(self, ctx, member: commands.MemberConverter):

        r = requests.get(f'https://nekos.life/api/v2/img/hug').json()
        url = r["url"]
        embed = discord.Embed(description=f"{ctx.author.mention} hugged {member.mention}", color=Customize.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(help='Make a funny tweet')
    async def tweet(self, ctx, username: str, *, message: str):
        r = await self.session.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message[:50]}") # [:50] trims the string to the first 50 characters (if it's longer than 50 characters)
        res = await r.json()
        await ctx.send(embed=Embed(color=0x36393d).set_image(url=res["message"]))
        await r.close(close_session=False)

    @commands.command(help='Make a funny tweet')
    async def ezx(self, ctx):

        await ctx.send(embed=Embed(title='d', color=0x36393d))
        

    @commands.command(help='Tickle a user')
    @commands.cooldown(3, 5, commands.BucketType.user)    
    async def tickle(self, ctx, member: commands.MemberConverter):
        r = requests.get(f'https://nekos.life/api/v2/img/tickle').json()
        url = r["url"]
        embed = discord.Embed(description=f"{ctx.author.mention} tickled {member.mention}", color=Customize.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(help='Sens a random comic')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def randomcomic(self, ctx):
        '''Get a comic from xkcd.'''
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://xkcd.com/info.0.json') as resp:
                data = await resp.json()
                currentcomic = data['num']
        rand = random.randint(0, currentcomic)  # max = current comic
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://xkcd.com/{rand}/info.0.json') as resp:
                data = await resp.json()
        em = discord.Embed(color=Customize.color)
        em.title = f"XKCD Number {data['num']}- \"{data['title']}\""
        em.set_footer(text=f"Published on {data['month']}/{data['day']}/{data['year']}")
        em.set_image(url=data['img'])
        await ctx.send(embed=em)
        
    @commands.command(help='Roll a dice')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dice(self, ctx, number=1):
        '''Rolls a certain number of dice'''
        if number > 20:
            number = 20

        fmt = ''
        for i in range(1, number + 1):
            fmt += f'`Dice {i}: {random.randint(1, 6)}`\n'
        em = discord.Embed(color=Customize.color, title='<:meidice:887296538022396014> | Dice Roll:', description=fmt)
        await ctx.send(embed=em)
        
    @commands.command(help='Sends a random joke')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def joke(self, ctx):
        response = requests.get('https://some-random-api.ml/joke') 
        data = response.json()
        joke = data['joke']
        embed = discord.Embed(
          title = 'Here is a joke',
          description = joke,
          color=Customize.color)
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed)   
            
    @commands.command(help='Pat said user')
    @commands.cooldown(3, 5, commands.BucketType.user)    
    async def pat(self, ctx, member: commands.MemberConverter):
        r = requests.get(f'https://nekos.life/api/v2/img/pat').json()
        url = r["url"]
        embed = discord.Embed(description=f"{ctx.author.mention} patted {member.mention}", color=Customize.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(help='Slap said user')
    @commands.cooldown(3, 5, commands.BucketType.user)  
    async def slap(self, ctx, member: commands.MemberConverter):
        r = requests.get(f'https://nekos.life/api/v2/img/slap').json()
        url = r["url"]
        embed = discord.Embed(description=f"{ctx.author.mention} slapped {member.mention}", color=Customize.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(help='Sends a random fact')
    @commands.cooldown(3, 5, commands.BucketType.user)   
    async def fact(self, ctx):
        r = requests.get(f'https://nekos.life/api/v2/fact').json()
        fact = r["fact"]
        await ctx.send(fact + ".")

    @commands.command(help='Ask the 8ball a question', name='8ball')
    @commands.cooldown(3, 5, commands.BucketType.user)    
    async def _8ball(self, ctx, *, question=None):
        if question is None:
            await ctx.send("You must provide a question for the 8ball to answer.")
        else:
            r = requests.get(f"https://nekos.life/api/v2/8ball").json()
            url = r["url"]
            desc = r["response"]
            embed = discord.Embed(title = "Answer:", color=Customize.color, description = desc)
            embed.set_image(url=url)
            embed.set_author(name=f"Question: {question}")
            await ctx.send(embed=embed)

    @commands.command(help='Feed said user')
    @commands.cooldown(3, 5, commands.BucketType.user)    
    async def feed(self, ctx, member: commands.MemberConverter):
        r = requests.get(f'https://nekos.life/api/v2/img/feed').json()
        url = r["url"]
        embed = discord.Embed(description=f"{ctx.author.mention} fed {member.mention}", color=Customize.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(help='Sends a random gif')
    @commands.cooldown(3, 14, BucketType.user)    
    async def gif(self, ctx,*,q="random"):
        api_key="kyFBqt0ZA68EMsAhO6XaNnYDBQdVuiBk"
        api_instance = giphy_client.DefaultApi()
        try: 
            api_response = api_instance.gifs_search_get(api_key, q, limit=50, rating='g')
            lst = list(api_response.data)
            giff = random.choice(lst)
            emb = discord.Embed(title="Random Gif", color=Customize.color)
            emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=emb)
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)    

    @commands.command(help='Searches for said gif')
    @commands.cooldown(3, 14, BucketType.user)    
    async def searchgif(self, ctx, *, q):
        api_key="kyFBqt0ZA68EMsAhO6XaNnYDBQdVuiBk"
        api_instance = giphy_client.DefaultApi()
        try:           
            api_response = api_instance.gifs_search_get(api_key, q, limit=50, rating='g')
            lst = list(api_response.data)
            giff = random.choice(lst)
            emb = discord.Embed(title="Your Searched Gif", color=Customize.color)
            emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.channel.send(embed=emb)
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)      
 
    @commands.command(help='Flip a coin')
    @commands.cooldown(3, 14, BucketType.user)    
    async def flip(self, ctx):
        number = (random.randint(1, 2))
        if number == 1:
            embed = discord.Embed(title = "Tails",description = "Coin Flipped!",color=Customize.color)
            embed.set_image(url = 'https://images-na.ssl-images-amazon.com/images/I/51NyMaKLydL._AC_.jpg')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title = "Heads",description = "Coin Flipped!",color=Customize.color)
            embed.set_image(url= "https://i.ebayimg.com/images/g/xtcAAOSwLwBaZigS/s-l300.jpg")
            await ctx.send(embed=embed)

    @commands.command(help='Sends a random meme')
    @commands.cooldown(3, 14, BucketType.user)    
    async def meme(self, ctx):
        await ctx.trigger_typing()
        r = requests.get("https://meme-api.herokuapp.com/gimme").json()
        postLink = str(r['postLink'])
        subreddit = str(r['subreddit'])
        caption = str(r['title'])
        image = str(r['url'])
        ups = str(r['ups'])
        embed = discord.Embed(title=f'{caption}', url=postLink, color=Customize.color)
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command(help='Sends a random lizard image')
    @commands.cooldown(3, 14, BucketType.user)   
    async def lizard(self, ctx):
        r = requests.get(f'https://nekos.life/api/v2/img/lizard').json()
        url = r["url"]
        embed = discord.Embed(description="Here is an image of a lizard", color=Customize.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(help='Sends a bunny picture')
    @commands.cooldown(3, 14, BucketType.user)  
    async def bunny(self, ctx):
        r = requests.get(f"https://api.bunnies.io/v2/loop/random/?media=gif,png").json()
        url = r["media"]["gif"]
        embed = discord.Embed(description="Here is an image of a bunny", color=Customize.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    
    @commands.command(help='Sends a random duck image')
    @commands.cooldown(3, 14, BucketType.user)  
    async def duck(self, ctx):
        r = requests.get(f"https://random-d.uk/api/v1/random?type=png").json()
        url = r["url"]
        embed = discord.Embed(description="Here is an image of a duck", color=Customize.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    
    @commands.command(help='Sends a random image of a Shiba')
    @commands.cooldown(3, 14, BucketType.user)   
    async def shiba(self, ctx):
        r = requests.get(f"http://shibe.online/api/shibes").json()
        url = r[0]
        embed = discord.Embed(description="Here is an image of a shiba", color=Customize.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def catfact(self, ctx):
        """Get a random fact about cats."""
        async with self.session.get("https://catfact.ninja/fact") as response:
            data = await response.json()
            fact = data["fact"]

            embed = discord.Embed(title = "Catfact", description = fact, color=Customize.color)
            await ctx.send(embed = embed)

    @commands.command()
    async def dogfact(self, ctx):
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://some-random-api.ml/facts/dog')
            factjson = await request2.json()
            embed = discord.Embed(description = factjson['fact'], color=Customize.color)
            await ctx.send(embed = embed)

    @commands.command(help="Shows a random quote")
    async def quote(self, ctx):
        async with aiohttp.ClientSession() as session:
            response = await session.get("https://zenquotes.io/api/random")
            json_data = json.loads(await response.text())
            quote = json_data[0]['q'] + " -" + json_data[0]['a']
            
        await ctx.send(quote)

    @commands.command(name="pong")
    async def pong(self, ctx):
        await ctx.send("pong... 🏓")

    @commands.command(name="nut")
    async def nut(self, ctx):
        await ctx.send("this is nuts ong 🥜 ")

    @commands.command(name="no")
    async def no(self, ctx):
        await ctx.send("no ma'am ⛔")

    @commands.command(name="lenny")
    async def lenny(self, ctx):
        await ctx.send("( ͡° ͜ʖ ͡°)")

    @commands.command(name="gn")
    async def gn(self, ctx):
        await ctx.send("good night my friend")

    @commands.command(name="gm")
    async def gm(self, ctx):
        await ctx.send("good morning my friend")

    @commands.command()    
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def randomnumber(self, ctx):
    	await ctx.send(f'{random.randint(1, 101)}')

    @commands.command()
    async def sadcat(self, ctx, song: str):
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=f"https://api.popcat.xyz/sadcat?text={song}")
        await ctx.send(embed=embed)

    @commands.command()
    async def oogway(self, ctx, song: str):
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=f"https://api.popcat.xyz/oogway?text={song}")
        await ctx.send(embed=embed)

    @commands.command()
    async def car(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.popcat.xyz/car") as r:
                data = await r.json()
                name = data['image']
                embed = discord.Embed(color=Customize.color)
                embed.set_image(url=f"{name}")
                await ctx.send(embed=embed)


    @commands.command()
    async def wanted(self, ctx, user: Optional[Union[discord.User, discord.Member]]):
        try:
            user = await self.bot.fetch_user(user.id)
        except AttributeError:
            user = ctx.author
    
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=f"https://api.popcat.xyz/wanted?image={user.avatar}")
        await ctx.send(embed=embed)

    @commands.command()
    async def gun(self, ctx, user: Optional[Union[discord.User, discord.Member]]):
        try:
            user = await self.bot.fetch_user(user.id)
        except AttributeError:
            user = ctx.author
    
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=f"https://api.popcat.xyz/gun?image={user.avatar}")
        await ctx.send(embed=embed)

    @commands.command()
    async def simp(self, ctx, user: Optional[Union[discord.User, discord.Member]]):
        try:
            user = await self.bot.fetch_user(user.id)
        except AttributeError:
            user = ctx.author
    
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=f"https://api.popcat.xyz/simpstamp?image={user.avatar}")
        await ctx.send(embed=embed)

    @commands.command()
    async def drip(self, ctx, user: Optional[Union[discord.User, discord.Member]]):
        try:
            user = await self.bot.fetch_user(user.id)
        except AttributeError:
            user = ctx.author
    
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=f"https://api.popcat.xyz/drip?image={user.avatar}")
        await ctx.send(embed=embed)

    @commands.command()
    async def uncover(self, ctx, user: Optional[Union[discord.User, discord.Member]]):
        try:
            user = await self.bot.fetch_user(user.id)
        except AttributeError:
            user = ctx.author
    
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=f"https://api.popcat.xyz/uncover?image={user.avatar}")
        await ctx.send(embed=embed)

    @commands.command()
    async def ad(self, ctx, user: Optional[Union[discord.User, discord.Member]]):
        try:
            user = await self.bot.fetch_user(user.id)
        except AttributeError:
            user = ctx.author
    
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=f"https://api.popcat.xyz/ad?image={user.avatar}")
        await ctx.send(embed=embed)

    @commands.command()
    async def blur(self, ctx, user: Optional[Union[discord.User, discord.Member]]):
        try:
            user = await self.bot.fetch_user(user.id)
        except AttributeError:
            user = ctx.author
    
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=f"https://api.popcat.xyz/blur?image={user.avatar}")
        await ctx.send(embed=embed)

    @commands.command()
    async def greyscale(self, ctx, user: Optional[Union[discord.User, discord.Member]]):
        try:
            user = await self.bot.fetch_user(user.id)
        except AttributeError:
            user = ctx.author
    
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=f"https://api.popcat.xyz/greyscale?image={user.avatar}")
        await ctx.send(embed=embed)


    @commands.command()
    async def mnm(self, ctx, user: Optional[Union[discord.User, discord.Member]]):
        try:
            user = await self.bot.fetch_user(user.id)
        except AttributeError:
            user = ctx.author
    
        embed = discord.Embed(color=Customize.color)
        embed.set_image(url=f"https://api.popcat.xyz/mnm?image={user.avatar}")
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Fun(bot))