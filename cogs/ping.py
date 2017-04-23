import discord
from .utils import checks


from discord.ext import commands

class Ping:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self):
        await self.bot.say("Pong.")

    @checks.is_owner()
    @commands.command(name='error', pass_context=True)
    async def _error(self, ctx):
        a = {}
        a['asd']

def setup(bot):
    bot.add_cog(Ping(bot))
