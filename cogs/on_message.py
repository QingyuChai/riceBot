import discord
from discord.ext import commands
import os
from .utils.dataIO import fileIO, dataIO
import asyncio

class Listener:
    def __init__(self, bot):
        self.bot = bot
        self.profile = "data/account/embed.json"
        self.riceCog = dataIO.load_json(self.profile)

    @commands.command(pass_context=True, aliases=['embed'])
    async def emb(self, ctx):
        yes_msg = "Embed_Messages has been enabled."
        no_msg = "Embed_Messages has been disabled."
        if 'toggle' not in self.riceCog:
            await self.bot.say(yes_msg)
            self.riceCog['toggle'] = 1
        elif self.riceCog['toggle'] == 1:
            self.riceCog['toggle'] = 0
            await self.bot.say(no_msg)
        elif self.riceCog['toggle'] == 0:
            await self.bot.say(yes_msg)
            self.riceCog['toggle'] = 1
        dataIO.save_json(self.profile, self.riceCog)



    async def on_message(self, message):
        new_msg = message.content
        if self.riceCog['toggle'] == 1:
            toggle = True
        if message.author.id == self.bot.user.id:
            pass
        else:
            return
        if message.content.lower() == "urw":
            await self.bot.edit_message(message, """I am the grain of my rice
Wheat is my body and water is my blood
I have fried over a thousand meals
Unknown to hunger
Nor known to malnutrition
Have let many full for the sake of...nothing.
Yet those mouths shall never taste anything
So, as I pray, Unlimited Rice Works""")
        if message.content.lower() == "!help":
            await self.bot.edit_message(message, "!help    *rip me*")
            new_msg = "!help    *rip me*"
        if "lenny" in message.content or message.content == "lenny":
            new_msg = message.content.replace("lenny", "( ͡° ͜ʖ ͡°)")
            await self.bot.edit_message(message, new_msg)
        if toggle:
            embed = discord.Embed(description = new_msg, colour=message.author.color)
            await self.bot.edit_message(message, new_content= " ", embed=embed)







def check_folder():
    if not os.path.exists("data/account"):
        print("Creating data/account/ folder")
        os.makedirs("data/account")

def check_file():
    data = {}
    f = "data/account/embed.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/account/embed.json")
        dataIO.save_json(f, data)




def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Listener(bot))
