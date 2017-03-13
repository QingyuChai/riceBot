import discord
import random
import os
import operator
from discord.utils import find

from .utils.dataIO import fileIO, dataIO
from discord.ext import commands

class Penis:
    def __init__(self, bot):
        self.bot = bot
        self.size = "data/account/penis.json"
        self.riceCog = dataIO.load_json(self.size)
        self._cog = self.bot.get_cog("Money")

    def _reset(self, author):
        user = author
        self.riceCog[user.id] = "="
        dataIO.save_json(self.size, self.riceCog)
        return "="

    def _boast(self, author):
        user = author
        return self.riceCog[user.id]

    @commands.command(pass_context=True, aliases=['wb'])
    async def wienerboard(self):
        users = []
        for userid in self.riceCog:
            for server in self.bot.servers:
                temp_user = find(lambda m: m.id == userid, server.members)
                if temp_user != None:
                    break
            if temp_user != None:
                users.append((temp_user.name, self.riceCog[temp_user.id]))
        sorted_list = sorted(users, key=operator.itemgetter(1), reverse=True)
        #print(sorted_list)
        #msg = ""
        #for pain in sorted_list:
        #    msg  += "\n".join(sorted_list)

        #await self.bot.say("\n".join(sorted_list))
        msg = "**Global Wienerboard for {}**\n".format(self.bot.user.name)
        msg += "```ruby\n"
        rank = 1
        labels = ["♔", "♕", "♖", "♗", "♘", "♙", " ", " ", " ", " "]
        for user in sorted_list[:10]:
            msg += u'{:<2}{:<2}{:<2}   # {:<5}\n'.format(rank, labels[rank-1], u"➤", user[0])
            msg += u'{:<2}{:<2}{:<2}    {:<5}\n'.format(" ", " ", " ", "8" + str(user[1]) + "D")
            rank += 1
        msg +="```"
        await self.bot.say(msg)


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
        if size < 1:
            await self.bot.say("Too smol.")
            return
        author = ctx.message.author
        user = author
        if author.id not in self.riceCog:
            await self.bot.say("Check your initial size first before deciding"
                               "to buy more!\nBe confident! "
                               "use **`{}penis`**!".format(ctx.prefix))
            return
        try:
            balance = self._cog._get_balance(author)
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
