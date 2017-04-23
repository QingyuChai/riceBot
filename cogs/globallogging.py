import discord
from discord import Object
from random import randint
from random import choice
urserverchannel = Object("294040185946243074")

class Globallogging:
    """Logs the bot's commands globally."""
    def __init__(self, bot):
        self.bot = bot
        self.commands = [command for command in self.bot.commands]


    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        prefixes = self.bot.settings.get_prefixes(message.server)
        for prefix in prefixes:
            if message.content.startswith(prefix):
                if message.content.replace(prefix, "").split(' ', 1)[0] in self.commands:
                    colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
                    colour = int(colour, 16)
                    author = message.author
                    embed = discord.Embed(description = "{}".format(author.id), colour=discord.Colour(value=colour))
                    embed.add_field(name="Server", value = "{}\n{}".format(message.server.name, message.server.id))
                    embed.add_field(name="Channel", value = "{}\n{}".format(message.channel.name, message.channel.id))
                    embed.add_field(name="Message", value=message.content, inline=False)
                    embed.set_thumbnail(url=message.server.icon_url)
                    embed.set_author(name="{}".format(author), icon_url=author.avatar_url)

                    await self.bot.send_message(urserverchannel, embed=embed)
                    break



def setup(bot):
    bot.add_cog(Globallogging(bot))
