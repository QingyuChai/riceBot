import asyncio
import discord
import os
import datetime
import json
import asyncio

from cogs.utils.dataIO import dataIO
from discord.ext import commands

print("<><><><><><><>")
print("--------------")
print("Starting up...")
print("--------------")
print("><><><><><><><")



token = "MTI0OTQ2ODMyMzA3NTE5NDky.C9v1Hw.f__DvNLEWb4UBhQmM1v0IR4M358"

rB = commands.Bot(command_prefix="s!", formatter=None, description=None, pm_help=False, self_bot=True)

@rB.event
async def on_ready():
    channel_count = 0
    user_count = 0
    for server in rB.servers:
        for channels in server.channels:
            channel_count += 1
        for user in server.members:
            user_count += 1
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("riceBot initializing... Please wait...")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Bot name: {}".format(rB.user.name))
    print("Bot ID: {}".format(rB.user.id))
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("{} servers.".format(len(rB.servers)))
    print("{} channels.".format(channel_count))
    print("{} users".format(user_count))
    print("{} cogs.".format(len(rB.cogs)))
    print("{} commands.".format(len(rB.commands)))
    print("{} Version: {}".format(discord.__title__, discord.__version__))
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    start_time = datetime.datetime.now()
    print("Current time is: {}".format(start_time))


@rB.event
async def on_message(message):
    if message.author.id != '124946832307519492':
        return
    if message.content == "test":
        await rB.edit_message(message, "testing...")
        await asyncio.sleep(1)
        await rB.edit_message(message, "testing done")
        return
    if message.content.startswith("s!"):
        #msg = message.content.replace("s!", "")
        #message_split = msg.split(" ")
        #com = message_split[0]
        #args = message_split[1:]

        await rB.process_commands(message)

@rB.event
async def send_error(ctx):
    px = ctx.prefix
    invoked = ctx.invoked_with
    com = rB.commands[invoked]
    args = " ".join(["{"+arg+"}" for arg in com.clean_params])
    msg = ("```asciidoc\n"
           "Error :: {com}\n\n"
           "{px}{com} {args}\n"
           "```")
    msg = msg.format(com=com,
                     px=px,
                     args=args)
    channel = ctx.message.channel
    await rB.send_message(channel, msg)

@rB.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel

    if isinstance(error, commands.MissingRequiredArgument):
        await rB.send_error(ctx)
    elif isinstance(error, commands.BadArgument):
        await rB.send_error(ctx)
    elif isinstance(error, commands.TooManyArguments):
        await rB.send_error(ctx)
    elif isinstance(error, commands.CommandNotFound):
        await rB.send_message(channel, "Sorry, command wasn't found.")
    elif isinstance(error, commands.CommandInvokeError):
        com = ctx.invoked_with
        msg = ctx.message.content.replace(ctx.prefix, "").replace(com, "")
        args = msg.split(' ')
        to_reply = ("```asciidoc\nAn exception was raised in command \"{com}\".\n\n"
                    "Command :: {px}{com}{args}\n"
                    "\nError: {type}\n{error}\n```")
        to_reply = to_reply.format(com=com,
                                   px=ctx.prefix,
                                   args=msg,
                                   type=type(error),
                                   error=error)
        await rB.send_message(channel, to_reply)


if not os.path.exists("data/cogs"):
    print("Creating data/cogs folder")
    os.makedirs("data/cogs")
data = {}
f = "loaded_cogs.json"
if not dataIO.is_valid_json(f):
    print("Creating data/account/warnings.json")
    dataIO.save_json(f, data)
cogs = "loaded_cogs.json"
riceCog = dataIO.load_json(cogs)

def _load_cogs():
    rB.load_extension('cogs.loader')
    #bot.load_extension('cogs.help')
    for cog in riceCog:
        if riceCog[cog] == True:
            rB.load_extension('cogs.{0}'.format(cog))

if __name__ == '__main__':
    _load_cogs()
    rB.run(token, bot=False)
