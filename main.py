import logging
import discord
from discord.ext import commands

from utils.utils import Methods
from utils.help import AsylumHelp
 
logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

bot = commands.Bot(
        command_prefix=Methods.get_prefix, 
        case_insensitive=True, 
        intents=discord.Intents.all(),
        help_command=AsylumHelp(),
        owner_ids={831171302336757790, 905121692978921472})

cogs = ["events.ReadyEvents", "events.AntiEvents", "events.AutoroleEvents", "events.GoodbyeEvents", "events.MiscEvents", "events.WelcomeEvents", "cogs.Configuration", "cogs.Fun", "cogs.Moderation", "cogs.Utility", "cogs.Jishaku", "cogs.InternalSystem"]

for cog in cogs:
    try:
        bot.load_extension(cog)
        logging.info(f"Successfully loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load {cog} with error: {e}")

if __name__ == "__main__":
    bot.run('xxx', reconnect=True)