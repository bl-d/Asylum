import pymongo
from discord.ext import commands
from utils.botcache import BotCache

class DataBase:
    mongoClient = pymongo.MongoClient('xxx')
    db1 = mongoClient.get_database("Springs").get_collection("servers_module")
    db3 = mongoClient.get_database("Springs").get_collection("welcome_module")
    db4 = mongoClient.get_database("Springs").get_collection("internal_module")
    db5 = mongoClient.get_database("Springs").get_collection("goodbye_module")
    db6 = mongoClient.get_database("Springs").get_collection("antinuke_module")
    db7 = mongoClient.get_database("Springs").get_collection("blacklist_module")
    db8 = mongoClient.get_database("Springs").get_collection("licenses")
    blacklist = db7['blacklist']
    blacklisted = db7['blacklist']

    def blacklist_check():
        def predicate(ctx):
            author_id = ctx.author.id
            if DataBase.blacklisted.find_one({'user_id': author_id}):
                return False
            return True

        return commands.check(predicate)

    def ServerSystem(server_id):
        DataBase.db1.insert_one({
            "guild_id": server_id,
            "prefix": '.',
            "premium": "No"
        })
        pass

    def WelcomeSystem(server_id):
        DataBase.db3.insert_one({
            "guild_id": server_id,
            "welcome_embed_toggle": 'Disabled',
            "welcome_embed_color": '0x747f8d',
            "welcome_embed_title": None,
            "welcome_embed_message": None,
            "welcome_toggle": 'Disabled',
            "welcome_message": None,
            "welcome_channel": None,
            "autorole_toggle": 'Disabled',
            "autoroles": []
        })
        pass

    def GoodbyeSystem(server_id):
        DataBase.db5.insert_one({
            "guild_id": server_id,
            "goodbye_embed_toggle": 'Disabled',
            "goodbye_embed_color": '0x747f8d',
            "goodbye_embed_title": None,
            "goodbye_embed_message": None,
            "goodbye_toggle": 'Disabled',
            "goodbye_message": None,
            "goodbye_channel": None
        })
        pass

    def AntiNukeSystem(server_id):
        DataBase.db6.insert_one({
            "guild_id": server_id,
            "whitelisted": [],
            "antiban_toggle": False,
            "antikick_toggle": False,
            "antirole_del_toggle": False,
            "antirole_create_toggle": False,
            "antichannel_del_toggle": False,
            "antichannel_create_toggle": False,
            "antiban_punishment": 'Ban',
            "antikick_punishment": 'Ban',
            "antirole_del_punishment": 'Ban',
            "antirole_create_punishment": 'Ban',
            "antichannel_del_punishment": 'Ban',
            "antichannel_create_punishment": 'Ban',
        })
        pass
