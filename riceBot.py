import asyncio
import discord
import os
import datetime
import json
import traceback
import asyncio

from cogs.utils.dataIO import fileIO, dataIO
from cogs.utils.chat_formatting import inline
from collections import Counter
from discord.ext import commands
from cogs.utils.settings import Settings

print("<><><><><><><>")
print("--------------")
print("Starting up...")
print("--------------")
print("><><><><><><><")



token = "MjcwNjQ0MDcyMjQxMjk5NDU2.C6Ygiw.fnyiPksWXyEEu7k2eNcEydgYw1A"

class Bot(commands.Bot):
    def __init__(self, command_prefix, formatter=None, description=None, pm_help=False, **options):

        super().__init__(command_prefix, formatter, description, pm_help, **options)
        self.token = token
        self._initialize_listeners()
        self.settings = Settings()

    async def send_cmd_help(self, ctx, command=None):
        msg = "**Command Help**"
        color = ctx.message.server.me.colour
        #[subcom for subcom in bot.commands['birthday'].commands]

        em=discord.Embed(description=msg, color=color)
        if command is not None:
            try:
                commie =  "```\n"
                commie += str(command)
                info = self.commands[command].help
                try:
                    sub_coms = ""
                    count = 0
                    for command in self.commands[command].commands:
                        if count == 0:
                            sub_coms += "`"+ str(command) + "`"
                            count += 1
                        else:
                            sub_coms += "-`" + str(command) + "`"
                except Exception as e:
                    print(e)
                commie += "\n```"
                em.add_field(name=commie, value=info, inline=False)
                if sub_coms:
                    em.add_field(name="Subcommands", value = sub_coms)
                em.set_footer(text="riceBot")
                await self.send_message(ctx.message.channel, embed=em)
            except Exception as e:
                print(e)
                await self.send_message(ctx.message.channel, "Couldn't find command! Try again.")

        elif ctx.invoked_subcommand:
            try:
                group = str(ctx.command).replace(" ", "")
                com_group = group.replace(str(ctx.subcommand_passed), "")
                args = [param for param in self.commands[com_group].commands[ctx.subcommand_passed].clean_params]
                print(com_group)
                print(ctx.subcommand_passed)
                #description = self.commands[str(ctx.command)].commands[str(ctx.invoked_subcommand)].description
                commie =  "```\n"
                commie += str(com_group) + " " + str(ctx.invoked_with) #+ str(description)
                for arg in args:
                    commie += " <{}>".format(arg)
                commie += "\n```"
                info = self.commands[str(com_group)].commands[str(ctx.subcommand_passed)].help
                em.add_field(name=commie, value=info, inline=False)
                em.set_footer(text="riceBot")
                await self.send_message(ctx.message.channel, embed=em)
            except Exception as e:
                print(e)
                await self.send_message(ctx.message.channel, "Couldn't find command! Try again.")
        else:
            try:
                description = ctx.command.description
                commie =  "```\n"
                commie += str(ctx.command) + str(description)
                info = self.commands[str(ctx.command)].help
                try:
                    sub_coms = ""
                    count = 0
                    for command in ctx.command.commands:
                        try:
                            params = [param for param in self.commands[commands].clean_params]
                        except:
                            pass
                        if count == 0:
                            sub_coms += "`"+ str(command)
                            if params:
                                for param in params:
                                    sub_coms += " {} ".format(param)
                            sub_coms += "`"
                            count += 1
                        else:
                            sub_coms += "-`" + str(command)
                            if params:
                                for param in params:
                                    sub_coms += " {} ".format(param)
                            sub_coms += "`"
                except Exception as e:
                    print(e)
                commie += "\n```"
                em.add_field(name=commie, value=info, inline=False)
                if sub_coms:
                    em.add_field(name="Subcommands", value = sub_coms)
                em.set_footer(text="riceBot")
                await self.send_message(ctx.message.channel, embed=em)
            except Exception as e:
                print(e)
                await self.send_message(ctx.message.channel, "Couldn't find command! Try again.")

    def _initialize_listeners(self):
        self.add_listener(self._startup_message, 'on_ready')

    async def _startup_message(self):
        channel = []
        server_count = 0
        channel_count = 0
        user_count = 0
        for server in self.servers:
            server_count += 1
            for channel in server.channels:
                channel_count += 1
            user_count += server.member_count
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("riceBot initializing... Please wait...")
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Bot name: {}".format(self.user.name))
        print("Bot ID: {}".format(self.user.id))
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("{} servers".format(server_count))
        print("{} channels".format(channel_count))
        print("{} users".format(user_count))
        print("{} cogs.".format(len(self.cogs)))
        print("{} commands.".format(len(self.commands)))
        print("Packages used: {} : {}".format(discord.__title__, discord.__version__))
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        self.start_time = datetime.datetime.now()
        print("Current time is: {}".format(self.start_time))

riceBot = Bot('r`', pm_help = True)
bot = riceBot

send_cmd_help = bot.send_cmd_help


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
    bot.load_extension('cogs.loader')
    #bot.load_extension('cogs.help')
    for cog in riceCog:
        if riceCog[cog] == True:
            bot.load_extension('cogs.{0}'.format(cog))

@bot.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    if isinstance(error, commands.MissingRequiredArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.BadArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(channel, "That command is disabled.")
    elif isinstance(error, commands.CommandInvokeError):
        logger.exception("Exception in command '{}'".format(
            ctx.command.qualified_name), exc_info=error.original)
        oneliner = "Error in command '{}' - {}: {}".format(
            ctx.command.qualified_name, type(error.original).__name__,
            str(error.original))
        await ctx.bot.send_message(channel, inline(oneliner))
    elif isinstance(error, commands.CommandNotFound):
        await bot.send_message(ctx.message.channel, "Command "
                                                    "not found.")
        pass
    elif isinstance(error, commands.CheckFailure):
        await bot.send_message(channel, "You do not have permission"
                                        " to use this command.")
    elif isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(channel, "That command is not "
                                        "available in DMs.")
    else:
        logger.exception(type(error).__name__, exc_info=error)

if __name__ == '__main__':
    _load_cogs()
    riceBot.run(token)
