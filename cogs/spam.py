import discord
import asyncio
import os

from __main__ import send_cmd_help
from .utils.chat_formatting import *
from .utils.dataIO import fileIO, dataIO
from .utils import checks
from discord.ext import commands

class Spam:
    def __init__(self, bot):
        self.bot = bot
        self.spam = "data/spam/spam.json"
        self.riceCog = dataIO.load_json(self.spam)

    @checks.is_owner()
    @commands.group(pass_context = True)
    async def spamlist(self, ctx):
        """List of users who can spam"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @commands.command(pass_context=True, name="spam")
    async def _spam(self, ctx, user : discord.Member, amount, *, msg):
        author = ctx.message.author
        server = ctx.message.server
        count = 0
        await self.bot.say("Please wait...")
        if author.id in self.riceCog and self.riceCog[author.id] == 1:
            await self.bot.send_message(user, "{} sends you his best regards.".format(author.name))
            if int(amount) < 11:
                while count < int(amount):
                    await self.bot.send_message(user, msg)
                    await asyncio.sleep(1)
                    count += 1
                await self.bot.send_message(user, "Congratulations on having been spammed {} messages by {}.".format(amount, user.name))
                await self.bot.say("Succesfully sent {} messages to {}.".format(amount, user.name))
            else:
                await self.bot.say("Sorry, too many messages.")
        else:
            await self.bot.say("You do not have permissions, fag.")


    @checks.is_owner()
    @spamlist.command(pass_context=True)
    async def add(self, ctx, user: discord.Member):
        if user.id not in self.riceCog:
            self.riceCog[user.id] = 1
            dataIO.save_json(self.spam, self.riceCog)
            await self.bot.say("{} added to the whitelist.".format(user.name))
        elif user.id in self.riceCog:
            if self.riceCog[user.id] == 1:
                await self.bot.say("User is already in the whitelist.")
                return
            self.riceCog[user.id] = 1
            dataIO.save_json(self.spam, self.riceCog)
            await self.bot.say("{} added to the whitelist.".format(user.name))

    @checks.is_owner()
    @spamlist.command(pass_context=True, alias=['del'])
    async def remove(self, ctx, user: discord.Member):
        if user.id in self.riceCog:
            if self.riceCog[user.id] == 0:
                await self.bot.say("User is not in the whitelist.")
                return
            self.riceCog[user.id] = 0
            dataIO.save_json(self.spam, self.riceCog)
            await self.bot.say("{} removed from the whitelist.".format(user.name))
        else:
            await self.bot.say("User is not in the whitelist.")


def check_folder():
    if not os.path.exists("data/spam"):
        print("Creating data/spam folder")
        os.makedirs("data/spam")

def check_file():
    data = {}
    f = "data/spam/spam.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/spam/spam.json")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Spam(bot))
