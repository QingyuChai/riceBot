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

    @commands.command(pass_context=True, name="help")
    async def _help(self, ctx, module : str = None):
        if not module:
            cogs = [cog for cog in self.bot.cogs]
            cogs.sort()
            try:
                colour = ctx.message.server.me.colour
            except:
                colour = 0x000000
            title = "{}help [module]".format(ctx.prefix)
            embed = discord.Embed(title=title, colour=colour)
            msg = ""
            for cog in cogs:
                if cog.lower() in blacklist:
                    continue
                msg += "{}\n".format(cog)
            embed.add_field(name="Modules", value=msg)
            await self.bot.say(embed=embed)
            return
        module = module.lower()
        #if ctx.message.author.id == '124946832307519492':
        #    pass
        #else:
        if module in blacklist:
            await self.bot.say("Sorry, that module does not exist.")
            return
        try:
            commands = [com for com in self.bot.commands if self.bot.commands[com].cog_name.lower() == module and com not in self.bot.commands[com].aliases]
            commands.sort()
            print(commands[0])
            try:
                colour = ctx.message.server.me.colour
            except:
                colour = 0x000000
            title = "Help for {}".format(module.title())
            embed = discord.Embed(title=title, colour=colour)
            msg = ""
            fag_params = ['self', 'ctx']
            for com in commands:
                msg += com
                for param in self.bot.commands[com].params:
                    if param in fag_params:
                        pass
                    else:
                        msg += " [{}]".format(param)
                msg += "\n"

            embed.add_field(name="Commands", value=msg)
            await self.bot.say(embed=embed)
        except Exception as e:
            print(e)
            await self.bot.say("Sorry, that module does not exist.")



def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
