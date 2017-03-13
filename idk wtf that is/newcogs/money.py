#New *money.py* cog based on economy
import discord
import os
import asyncio
import datetime
import operator

from discord.utils import find
from __main__ import send_cmd_help
from .utils.chat_formatting import *
from .utils.dataIO import fileIO, dataIO
from .utils import checks
from discord.ext import commands

class Leaderboard_Person(object):
    id = ""
    count = 0
    balance = 0



class Money:
    def __init__(self, bot):
        self.bot = bot
        self._money = "data/money/account.json"
        self.riceCog = dataIO.load_json(self._money)
        for user in self.riceCog:
            self.riceCog[user]["wait"] = False
        dataIO.save_json(self._money, self.riceCog)

    def _check_user(self, user):
        if str(user.id) in self.riceCog:
            return True
        else:
            return False

    def _get_balance(self, user):
        balance = self.riceCog[user.id]["balance"]
        return balance

    def _substract_money(self, user, amount):
        balance = self.riceCog[user.id]["balance"]
        balance -= amount
        self.riceCog[user.id].update({"balance" : balance})
        dataIO.save_json(self._money, self.riceCog)

    def _add_money(self, user, amount):
        balance = self.riceCog[user.id]["balance"]
        balance += amount
        self.riceCog[user.id].update({"balance" : balance})
        dataIO.save_json(self._money, self.riceCog)



    @commands.group(pass_context=True)
    async def money(self, ctx):
        """
        Birthday options"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @commands.command(pass_context=True, name="setbalance", aliases=["balanceset"])
    @checks.is_owner()
    async def _setbalance(self, ctx, riceGrains : int, user : discord.Member = None):
        if user == None:
            user = ctx.message.author
        prefix = ctx.prefix
        if user.id not in self.riceCog:
            await self.bot.say("{} did not register yet! Use **{}bankopen**!".format(user.mention, prefix))
            return
        self.riceCog[user.id]["balance"] = riceGrains
        user_balance = riceGrains
        await self.bot.say("{} has a balance of {} riceGrains now!".format(user.name, user_balance))
        dataIO.save_json(self._money, self.riceCog)

    @commands.command(pass_context=True, name="balance", aliases=["bankbalance", "bb"])
    async def _balance(self, ctx, user : discord.Member = None):
        if user == None:
            user = ctx.message.author
        prefix = ctx.prefix
        if user.id not in self.riceCog:
            await self.bot.say("You did not register yet! Use **{}bankopen**!".format(prefix))
            return
        user_balance = self.riceCog[user.id]["balance"]
        await self.bot.say("{} has a balance of {} riceGrains!".format(user.name, user_balance))

    @commands.command(pass_context=True, name="payday", aliases=["pd"])
    async def _payday(self, ctx):
        author = ctx.message.author
        server = ctx.message.server
        prefix = ctx.prefix
        user = author
        if user.id in self.riceCog:
            payday_wait = self.riceCog[user.id]["wait"]
            if payday_wait == True:
                now = datetime.datetime.now()
                hour = now.hour
                minute = now.minute
                second = now.second
                total_time = 3600 * hour + 60 * minute + second
                self.riceCog[user.id].update({"wait" : True})
                previous_time = self.riceCog[user.id]["time"]
                timer = total_time - previous_time
                timer = 300 - timer
                await self.bot.say("Sorry, you need to wait {} seconds until your next payday!".format(timer))
                await asyncio.sleep(20)
                self.riceCog[user.id].update({"count" : 0})
                return
            self.riceCog[user.id]["balance"] += 500
            user_balance = self.riceCog[user.id]["balance"]
            await self.bot.say("You succesfully added 500 riceGrains to your account balance!")
            await self.bot.say("Your current balance is: {} riceGrains!".format(user_balance))
        else:
            await self.bot.say("You did not register yet! Use **{}bankopen**!".format(prefix))
            payday_wait = "False"
            return
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        total_time = 3600 * hour + 60 * minute + second
        self.riceCog[user.id].update({"wait" : True})
        self.riceCog[user.id].update({"time" : total_time})
        self.riceCog[user.id].update({"count" : 0})
        dataIO.save_json(self._money, self.riceCog)
        await asyncio.sleep(300)
        self.riceCog[user.id].update({"wait" : False})
        dataIO.save_json(self._money, self.riceCog)

    @commands.command(pass_context=True, name="bankopen", aliases=["openbank", "bankregister", "registerbank"])
    async def _bankopen(self, ctx):
        author = ctx.message.author
        if author.id in self.riceCog:
            await self.bot.say("You already registered, {}!".format(author.mention))
            return
        self.riceCog[author.id] = {}
        self.riceCog[author.id].update({"balance" : 500})
        self.riceCog[author.id].update({"wait" : False})
        user_balance = self.riceCog[author.id]["balance"]
        msg = "You have succesfully registered!\n"
        msg += "Your current balance is: {} riceGrains!".format(user_balance)
        await self.bot.say(msg)
        dataIO.save_json(self._money, self.riceCog)

    @commands.command(pass_context=True)
    async def ranking(self, ctx, margin=None):
    #    global_ranking = {}
    #    for userid in self.riceCog:
    #        first_user = Leaderboard_Person()
    #        first_user.count = 0
    #        first_user.id = userid
    #        first_user.balance = self.riceCog[userid]
    #            if userid == userid_2:
    #                continue
    #            second_user = Leaderboard_Person()
    #            second_user.id = userid_2
    #            second_user.balance = self.riceCog[userid_2]
    #            if first_user.balance > second_user.balance:
    #                count = int(first_user.count) + 1
    #                first_user.count = str(count)
    #            else:
    #                continue
    #        global_ranking[first_user.count] = first_user
    #    print(global_ranking)
        users = []
        for userid in self.riceCog:
            for server in self.bot.servers:
                temp_user = find(lambda m: m.id == userid, server.members)
                if temp_user != None:
                    break
            if temp_user != None:
                users.append((temp_user.name, self.riceCog[temp_user.id]["balance"]))
        sorted_list = sorted(users, key=operator.itemgetter(1), reverse=True)
        #print(sorted_list)
        #msg = ""
        #for pain in sorted_list:
        #    msg  += "\n".join(sorted_list)

        #await self.bot.say("\n".join(sorted_list))
        msg = "**Global Bank Leaderboard for {}**\n".format(self.bot.user.name)
        msg += "```ruby\n"
        rank = 1
        labels = ["♔", "♕", "♖", "♗", "♘", "♙", " ", " ", " ", " "]
        for user in sorted_list[:10]:
            msg += u'{:<2}{:<2}{:<2}   # {:<5}\n'.format(rank, labels[rank-1], u"➤", user[0])
            msg += u'{:<2}{:<2}{:<2}    {:<5}\n'.format(" ", " ", " ", "Total Balance: " + str(user[1]) + " riceGrains!")
            rank += 1
        msg +="```"
        await self.bot.say(msg)
def check_folder():
    if not os.path.exists("data/money"):
        print("Creating data/money folder")
        os.makedirs("data/money")

def check_file():
    data = {}
    f = "data/money/account.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/money/account.json")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    n = Money(bot)
    bot.add_cog(n)
