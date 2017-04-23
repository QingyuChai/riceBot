#New *money.py* cog based on economy
import discord
import os
import asyncio
import operator
import random
import time
NUM_ENC = "\N{COMBINING ENCLOSING KEYCAP}"
import datetime
from datetime import datetime as fuckingdate
from collections import namedtuple, defaultdict, deque
from discord.utils import find
from __main__ import send_cmd_help
from .utils.chat_formatting import *
from .utils.dataIO import fileIO, dataIO
from .utils import checks
from discord.ext import commands
from enum import Enum

class SMReel(Enum):
    cherries  = "\N{CHERRIES}"
    cookie    = "\N{COOKIE}"
    two       = "\N{DIGIT TWO}" + NUM_ENC
    flc       = "\N{FOUR LEAF CLOVER}"
    cyclone   = "\N{CYCLONE}"
    sunflower = "\N{SUNFLOWER}"
    six       = "\N{DIGIT SIX}" + NUM_ENC
    mushroom  = "\N{MUSHROOM}"
    heart     = "\N{HEAVY BLACK HEART}"
    snowflake = "\N{SNOWFLAKE}"

PAYOUTS = {
    (SMReel.two, SMReel.two, SMReel.six) : {
        "payout" : lambda x: x * 2500 + x,
        "phrase" : "JACKPOT! 226! Your bid has been multiplied * 2500!"
    },
    (SMReel.flc, SMReel.flc, SMReel.flc) : {
        "payout" : lambda x: x + 1000,
        "phrase" : "4LC! +1000!"
    },
    (SMReel.cherries, SMReel.cherries, SMReel.cherries) : {
        "payout" : lambda x: x + 800,
        "phrase" : "Three cherries! +800!"
    },
    (SMReel.two, SMReel.six) : {
        "payout" : lambda x: x * 4 + x,
        "phrase" : "2 6! Your bid has been multiplied * 4!"
    },
    (SMReel.cherries, SMReel.cherries) : {
        "payout" : lambda x: x * 3 + x,
        "phrase" : "Two cherries! Your bid has been multiplied * 3!"
    },
    "3 symbols" : {
        "payout" : lambda x: x + 500,
        "phrase" : "Three symbols! +500!"
    },
    "2 symbols" : {
        "payout" : lambda x: x * 2 + x,
        "phrase" : "Two consecutive symbols! Your bid has been multiplied * 2!"
    },
}

default_settings = {"PAYDAY_TIME": 300, "PAYDAY_CREDITS": 500,
                    "SLOT_MIN": 100, "SLOT_MAX": 50000, "SLOT_TIME": 5,
                    "REGISTER_CREDITS": 500}

SLOT_PAYOUTS_MSG = ("Slot machine payouts:\n"
                    "{two.value} {two.value} {six.value} Bet * 2500\n"
                    "{flc.value} {flc.value} {flc.value} +1000\n"
                    "{cherries.value} {cherries.value} {cherries.value} +800\n"
                    "{two.value} {six.value} Bet * 4\n"
                    "{cherries.value} {cherries.value} Bet * 3\n\n"
                    "Three symbols: +500\n"
                    "Two symbols: Bet * 2".format(**SMReel.__dict__))

class Leaderboard_Person(object):
    id = ""
    count = 0
    balance = 0

class EconomyError(Exception):
    pass

class BankError(Exception):
    pass

class OnCooldown(EconomyError):
    pass


class InvalidBid(EconomyError):
    pass



class Money:
    def __init__(self, bot):
        global default_settings
        self.bot = bot
        self._money = "data/money/account.json"
        self.riceCog = dataIO.load_json(self._money)
        for user in self.riceCog:
            self.riceCog[user]["wait"] = False
        dataIO.save_json(self._money, self.riceCog)
        self.file_path = "data/economy/settings.json"
        self.settings = dataIO.load_json(self.file_path)
        if "PAYDAY_TIME" in self.settings:  # old format
            default_settings = self.settings
            self.settings = {}
        self.settings = defaultdict(lambda: default_settings, self.settings)
        self.payday_register = defaultdict(dict)
        self.slot_register = defaultdict(dict)

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



    async def slot_machine(self, author, bid):
        default_reel = deque(SMReel)
        reels = []
        self.slot_register[author.id] = fuckingdate.utcnow()
        for i in range(3):
            default_reel.rotate(random.randint(-999, 999)) # weeeeee
            new_reel = deque(default_reel, maxlen=3) # we need only 3 symbols
            reels.append(new_reel)                   # for each reel
        rows = ((reels[0][0], reels[1][0], reels[2][0]),
                (reels[0][1], reels[1][1], reels[2][1]),
                (reels[0][2], reels[1][2], reels[2][2]))

        slot = "~~\n~~" # Mobile friendly
        for i, row in enumerate(rows): # Let's build the slot to show
            sign = "  "
            if i == 1:
                sign = ">"
            slot += "{}{} {} {}\n".format(sign, *[c.value for c in row])

        payout = PAYOUTS.get(rows[1])
        if not payout:
            # Checks for two-consecutive-symbols special rewards
            payout = PAYOUTS.get((rows[1][0], rows[1][1]),
                     PAYOUTS.get((rows[1][1], rows[1][2]))
                                )
        if not payout:
            # Still nothing. Let's check for 3 generic same symbols
            # or 2 consecutive symbols
            has_three = rows[1][0] == rows[1][1] == rows[1][2]
            has_two = (rows[1][0] == rows[1][1]) or (rows[1][1] == rows[1][0])
            if has_three:
                payout = PAYOUTS["3 symbols"]
            elif has_two:
                payout = PAYOUTS["2 symbols"]

        if payout:
            then = self._get_balance(author)
            pay = payout["payout"](bid)
            now = then - bid + pay
            self.riceCog[user.id]["balance"] = now
            dataIO.save_json(self._money, self.riceCog)
            await self.bot.say("{}\n{} {}\n\nYour bid: {}\n{} → {}!"
                               "".format(slot, author.mention,
                                         payout["phrase"], bid, then, now))
        else:
            then = self._get_balance(author)
            self._substract_money(author, bid)
            now = then - bid
            await self.bot.say("{}\n{} Nothing!\nYour bid: {}\n{} → {}!"
                               "".format(slot, author.mention, bid, then, now))

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

    @commands.command(pass_context=True, no_pm=True, aliases=['slots'])
    async def slot(self, ctx, bid: int):
        """Play the slot machine"""
        author = ctx.message.author
        server = author.server
        settings = self.settings[server.id]
        valid_bid = settings["SLOT_MIN"] <= bid and bid <= settings["SLOT_MAX"]
        slot_time = settings["SLOT_TIME"]
        last_slot = self.slot_register.get(author.id)
        now = fuckingdate.utcnow()
        user = author
        async def _check_user(self, ctx, user):
            if str(user.id) in self.riceCog:
                return True
            else:
                return False
        if not await _check_user(self, ctx, author):
            await self.bot.say("Register first using **`{}bankopen`**!".format(ctx.prefix))
        if bid > self.riceCog[user.id]["balance"]:
            await self.bot.say("You don't have enough money!")
            return

        try:
            if last_slot:
                if (now - last_slot).seconds < slot_time:
                    raise OnCooldown()
            if not valid_bid:
                raise InvalidBid()
            if bid > self.riceCog[user.id]["balance"]:
                await self.bot.say("You do not have enough money!")
                return
            await self.slot_machine(author, bid)
        except OnCooldown:
            await self.bot.say("Slot machine is still cooling off! Wait {} "
                               "seconds between each pull".format(slot_time))
        except InvalidBid:
            await self.bot.say("Bid must be between {} and {}."
                               "".format(settings["SLOT_MIN"],
                                         settings["SLOT_MAX"]))

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
        await self.bot.send_message(user, "{}, your next payday is ready!".format(user.mention))
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
