import discord
import os
import collections
from .utils.dataIO import fileIO, dataIO
from .utils import checks
from discord.ext import commands
blacklist = ['customcommands', 'config', 'cleverbot','downloader','globalalias','help','owner','repl','terminal','ping','loader']
class Help:
    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command(pass_context=True, name="help")
    async def _help(self, ctx, module : str = None):
        coms = ['"{}"'.format(com) for com in self.bot.commands]
        msg = "```python\n"
        msg += "~".join(coms)
        msg += "```"
        await self.bot.say(msg)



def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
