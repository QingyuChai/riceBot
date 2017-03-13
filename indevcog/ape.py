import discord


from discord.ext import commands

class ape:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whoisape(self):
        await self.bot.say("You " + "are the ape, you boosted bonobo!")

def setup(bot):
    bot.add_cog(ape(bot))