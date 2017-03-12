import discord
import os
import collections
from .utils.dataIO import fileIO, dataIO
from .utils import checks
from discord.ext import commands

class Help:
    def __init__(self, bot):
        self.bot = bot
        self.profile = "data/help/toggle.json"
        self.riceCog = dataIO.load_json(self.profile)

    @commands.command(pass_context=True, name="help")
    async def _help(self, ctx, module : str = None):
        if not module:
            cogs = [cog for cog in self.bot.cogs]
            await self.bot.say(cogs)
            return
        module = module.lower()
        try:
            commands = [com for com in self.bot.commands if self.bot.commands[com].cog_name.lower() == module]
            print(commands[1])
            await self.bot.say(commands)
        except:
            await self.bot.say("Sorry, that module does not exist.")



def check_folder():
    if not os.path.exists("data/help"):
        print("Creating data/help folder")
        os.makedirs("data/help")

def check_file():
    data = {}
    f = "data/help/toggle.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/help/toggle.json")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    bot.remove_command('help')
    bot.add_cog(Help(bot))
