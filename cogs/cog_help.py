import discord
import os
import collections
from .utils.dataIO import fileIO, dataIO
from .utils import checks
from discord.ext import commands

class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="help")
    async def _help(self, ctx, module : str = None):
        if not module:
            cogs = [cog for cog in self.bot.cogs]
            cogs.sort()
            try:
                colour = ctx.message.author.colour
            except:
                colour = 0x000000
            print(1)
            title = "{}help [module]".format(ctx.prefix)
            embed = discord.Embed(title=title, colour=colour)
            msg = ""
            descr = ""
            print(2)
            for cog in cogs:
                msg += "{}\n".format(cog)
                descr += "{}\n".format(cog.__doc__)
            print(3)
            embed.add_field(name="Modules", value=msg)
            print(4)
            print(5)
            await self.bot.say(embed=embed)
            return
        module = module.lower()
        try:
            commands = [com for com in self.bot.commands if self.bot.commands[com].cog_name.lower() == module]
            commands.sort()
            print(commands[0])
            await self.bot.say(commands)
        except:
            await self.bot.say("Sorry, that module does not exist.")



def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
