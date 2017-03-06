import discord


from discord.ext import commands

class template:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def template(self):
        await self.bot.say("http://pastebin.com/ixmZ4TTp", tts=False)

def setup(bot):
    bot.add_cog(template(bot))