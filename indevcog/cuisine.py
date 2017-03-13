import discord
import os
import asyncio

from copy import deepcopy
from .utils.dataIO import fileIO, dataIO
from discord.ext import commands
from __main__ import send_cmd_help


class Cuisine:
    def __init__(self, bot):
        self.bot = bot
        self._money = "data/money/account.json"
        self.riceCog = dataIO.load_json(self._money)
        for user in self.riceCog:
            self.riceCog[user]["food"] = False

    @commands.group(pass_context = True)
    async def order(self, ctx, food, amount):
        """Ordering help"""
        #Get the subcommand
        user = ctx.message.author
        server = ctx.message.server
        prefix = ctx.prefix
        food = food #kek

        #Connect to money cog
        _cog = self.bot.get_cog("Money")

        #Checks if user has an account
        user_exists = _cog._check_user(user)

        if user_exists == False:
            await self.bot.say("You do not have an account, {}!".format(user.mention))
            return

        amount = int(amount)

        food_list = ["rice", "noodles"]

        if food not in food_list:
            await self.bot.say("Sorry, we don't serve this here!")
            return

        #Checks if there is an order going on right now
        if self.riceCog[user.id]["food"]:
            await self.bot.say("You have an order going on!")
            return

        balance = _cog._get_balance(user)

        if amount < 1:
            await self.bot.say("Try again!")
            return

        cost = amount
        #Declare food
        if food == "rice":
            food = "grain(s) of rice!"
        elif food == "noodles":
            food = "string(s) of noodles!"
            cost = amount * 2


        #Basically changing variable name
        if cost > balance:
            await self.bot.say("You are too poor to afford this.")
            return

        #Get the function from the other cog
        _cog._substract_money(user, cost)

        #Waiting sequence
        await self.bot.say("You have succesfully ordered {} {}!".format(amount, food))
        await self.bot.say("Please wait a bit while we prepare the food...")
        self.riceCog[user.id]["food"] = True
        await asyncio.sleep(60)
        await self.bot.say("Food has been made. Delivering...")
        await asyncio.sleep(60)
        self.riceCog[user.id]["food"] = False
        await self.bot.say("Here are your {} grains of rice, {}!".format(amount, user.mention))






def check_files():
    f = "data/money/account.json"
    if not dataIO.is_valid_json(f):
        return


def setup(bot):
    check_files()
    if check_files() == False:
        return
    bot.add_cog(Cuisine(bot))
