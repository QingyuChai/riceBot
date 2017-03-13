import discord

from discord.ext import commands
from __main__ import settings

class Listener:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        channel = message.channel
        author = message.author
        if message.content == "size pls".lower():
            _cog = self.bot.get_cog("Penis")
            try:
                size = _cog._boast(author)
                await self.bot.send_message(channel, "Your size is 8{}D,"
                                            " how tiny.".format(size))
            except:
                await self.bot.send_message(channel, "Set your penis "
                                            "with **r!penis** first!")

        elif message.content == "balance pls".lower():
            _cog = self.bot.get_cog("Money")
            balance = _cog._get_balance(author)
            await self.bot.send_message(channel, "Your balance is {} riceGrains,"
                                        " you poor fuck.".format(balance))
        if message.author.id == self.bot.settings.owner or message.author.id == '95645231248048128':
            pass
        else:
            return
        if message.content == "ricebot!".lower():
            await self.bot.send_message(channel, "Hello there, Boss!")
        elif message.content == "laif".lower():
            await self.bot.send_message(channel, "No waifu no laifu.")
        elif message.content == "reset penis pls".lower():
            _cog = self.bot.get_cog("Penis")
            feels_reset_man = _cog._reset(author)
            await self.bot.send_message(channel, "Your size is now"
                                        " 8{}D.".format(feels_reset_man))
        elif message.content == "make it rain".lower():
            _cog = self.bot.get_cog("Money")
            _cog._add_money(author, 5000)
            balance = _cog._get_balance(author)
            await self.bot.send_message(channel, "You have received 5000 "
                                        "riceGrains.\nYour balance is now {}"
                                        " riceGrains.".format(balance))
        elif message.content == "die pls".lower() and message.author.id == self.bot.settings.owner:
            await self.bot.send_message(message.channel, "Pls no hurt me!")
            await self.bot.shutdown()


        else:
            return


def setup(bot):
    bot.add_cog(Listener(bot))
