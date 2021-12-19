from cogs.jishaku.cog import *
from utils.utils import Methods
from utils.help import AsylumHelp
from utils.botcache import BotCache
from utils.database import DataBase
from utils.paginator import *
from utils.utils import *

from colorama import Fore as C


def setup(bot):
    bot.add_cog(Jishaku(bot=bot))