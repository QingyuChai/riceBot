import discord


from discord.ext import commands

class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', pass_context=True)
    async def _help(self, ctx):
        self.bot.commands[str(ctx.command)].class_name = 'Help'
        msg = "Command list: \n"
        await self.bot.say("Hello.")
        for com in self.bot.commands:
            try:
                msg += "{} - {}\n".format(self.bot.commands[com].class_name, com)

            except:
                continue
        await self.bot.say(msg)


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Danger(bot))
