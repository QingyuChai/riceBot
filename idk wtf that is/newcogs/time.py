import discord


from discord.ext import commands

class time:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def time(self):
        await self.bot.say("It's wank time!")

def setup(bot):
    bot.add_cog(time(bot))