import discord
import random
import os

from .utils.dataIO import fileIO, dataIO
from discord.ext import commands

class Penis:
    def __init__(self, bot):
        self.bot = bot
        self.size = "data/account/penis.json"
        self.riceCog = dataIO.load_json(self.size)
        self._cog = self.bot.get_cog("Money")


    @commands.command(pass_context=True)
    async def penis(self, ctx, user : discord.Member = None):
        if user == None:
            user = ctx.message.author
        p = "="
        if user.id not in self.riceCog:
            self.riceCog[user.id] = p
        else:
            p = self.riceCog[user.id]
        p = "8" + p + "D"
        dataIO.save_json(self.size, self.riceCog)
        await self.bot.say("Size: \n" + p)

    @commands.command(pass_context=True)
    async def buysize(self, ctx, size : int):
        """
        Price for an increase of one **size** is 1000 riceGrains.
        """
        author = ctx.message.author
        user = author
        if author.id not in self.riceCog:
            await self.bot.say("Check your initial size first before deciding"
                               "to buy more!\nBe confident! "
                               "use **`{}penis`**!".format(ctx.prefix))
            return
        try:
            balance = self._cog._check_user(author)
        except:
            await self.bot.say("You need to register a bank account first! Use "
                               "**`{}bankopen`**".format(ctx.prefix))
            return
        p = self.riceCog[author.id]
        price = 1000 * size
        balance = self._cog._get_balance(author)
        if price > balance:
            await self.bot.say("Sorry, you can't afford that size.")
            return
        else:
            self._cog._substract_money(author, price)
            balance = self._cog._get_balance(author)
            i = 0
            while i < size:
                p += "="
                i += 1
            self.riceCog[user.id] = p
            dataIO.save_json(self.size, self.riceCog)
            penis_size = "8" + p + "D"
            await self.bot.say("Congratulations! Your penis is now this:"
                               "\n{}"
                               "\nYou payed {}. You are now left with {} "
                               "riceGrains.".format(penis_size, price, balance))



def check_folder():
    if not os.path.exists("data/account"):
        print("Creating data/account folder")
        os.makedirs("data/account")

def check_file():
    data = {}
    f = "data/account/penis.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/account/penis.json")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    bot.remove_command("buysize")
    bot.remove_command("penis")
    bot.add_cog(Penis(bot))
