import checks
import discord
import json
import datetime
import asyncio
import time

from os import listdir
from os.path import isfile, join
from discord.ext import commands
import checks
from .utils.dataIO import fileIO, dataIO
from cogs.utils import checks
from cogs.utils.chat_formatting import pagify, box
from subprocess import check_output, CalledProcessError
from platform import system, release
from os import name



class Loader():
    def __init__(self, bot):
        self.bot = bot
        self.cogs = "loaded_cogs.json"
        self.riceCog = dataIO.load_json(self.cogs)


    @commands.command()
    @checks.is_owner()
    async def os(self):
        """Displays your current Operating System"""

        await self.bot.say(box(system() + "\n" + release(), 'Bash'))

    @commands.command()
    @checks.is_owner()
    async def osname(self):
        """Displays your current Operating System name"""

        await self.bot.say(box(system(), 'Bash'))

    @commands.command(alias=["osver"])
    @checks.is_owner()
    async def osversion(self):
        """Displays your current Operating System version"""

        await self.bot.say(box(release(), 'Bash'))

    @commands.command(aliases=["cmd", "terminal"])
    @checks.is_owner()
    async def shell(self, *, command: str):
        """Terminal inside Discord"""

        # List of blocked commands
        blacklist = []

        if command.find("&") != -1:
            command = command.split("&")[0]

        for x in blacklist:
            if command.lower().find(x) != -1:
                await self.bot.say("You cannot execute '{}'".format(command))
                return

        if command.lower().find("apt-get") != -1 and command.lower().find("-y") == -1:
            command = "{} -y".format(command)

        try:
            output = check_output(command, shell=True)
            error = False
        except CalledProcessError as e:
            output = e.output
            error = True

        # Decode to unicode for full character support
        shell = output.decode('utf_8')

        if shell == "" and not error:
            # in the case no output is given but no error has happened
            return
        elif shell == "" and error:
            # debug error. Some commands like sudo will resolve to this
            shell = "a error has occured"

        for page in pagify(shell, shorten_by=20):
            await self.bot.say(box(page, 'Prolog'))

    @checks.is_owner()
    @commands.command(name='shutdown', hidden=True)
    async def _shutdown(self):
        await self.bot.say("Shutting down...")
        await self.bot.close()

    @checks.is_owner()
    @commands.command()
    async def cogfolder(self):
        onlyfiles = [f for f in listdir("cogs")]
        count = 0
        msg = ""
        for _file in onlyfiles:
            if count == 0:
                msg += "`{}`".format(_file)
                count += 1
            else:
                msg += "~`{}`".format(_file)
        await self.bot.say(msg)

    @checks.is_owner()
    @commands.command(name='cogs', pass_context=True)
    async def _cogs(self, ctx):
        await self.bot.say("{} cogs loaded.".format(len(self.bot.cogs)))
        msg = ""
        count = 0
        for cog in self.bot.cogs:
            if count == 0:
                msg += "`{}`".format(cog.replace("cogs.", ""))
                count += 1
            else:
                msg += "~`{}`".format(cog.replace("cogs.", ""))
        await self.bot.say(msg)

    @checks.is_owner()
    @commands.command(pass_context=True)
    async def load(self, ctx, module):
        try:
            info = {module : True}
            self.bot.load_extension('cogs.{}'.format(module))
            self.riceCog[module] = True
            dataIO.save_json(self.cogs, self.riceCog)
            await self.bot.say("Sucess! Loaded module: {}.".format(module))
        except Exception as e:
            print(e)
            print(datetime.datetime.now())
            await self.bot.say("Sorry, couldn't load module.")
        except:
            await self.bot.say("Sorry, couldn't load module.")

    @checks.is_owner()
    @commands.command(pass_context=True)
    async def unload(self, ctx, module):
        try:
            self.bot.unload_extension('cogs.{}'.format(module))
            await self.bot.say("Sucess! Unloaded module: {}.".format(module))
            self.riceCog[module] = False
            dataIO.save_json(self.cogs, self.riceCog)
        except Exception as e:
            print(e)
            print(datetime.datetime.now())

    @checks.is_owner()
    @commands.command(pass_context=True)
    async def reload(self, ctx, module):
        try:
            self.bot.unload_extension('cogs.{}'.format(module))
            self.bot.load_extension('cogs.{}'.format(module))
            await self.bot.say("Sucess! Reloaded module: {}".format(module))
            self.riceCog[module] = True
            dataIO.save_json(self.cogs, self.riceCog)
        except Exception as e:
            await self.bot.say("Sorry, couldn't reload module.")
            print(e)
            print(datetime.datetime.now())

    @checks.is_owner()
    @commands.command(pass_context=True, hidden=True)
    async def debug(self, ctx, *, code):
        """Evaluates code"""
        def check(m):
            if m.content.strip().lower() == "more":
                return True

        author = ctx.message.author
        channel = ctx.message.channel

        code = code.strip('` ')
        result = None

        global_vars = globals().copy()
        global_vars['bot'] = self.bot
        global_vars['ctx'] = ctx
        global_vars['message'] = ctx.message
        global_vars['author'] = ctx.message.author
        global_vars['channel'] = ctx.message.channel
        global_vars['server'] = ctx.message.server

        try:
            result = eval(code, global_vars, locals())
        except Exception as e:
            await self.bot.say("```python\n" + ('{}: {}\n```'.format(type(e).__name__, str(e))))
            return

        if asyncio.iscoroutine(result):
            result = await result

        result = str(result)


        result = list(pagify(result, shorten_by=16))

        for i, page in enumerate(result):
            if i != 0 and i % 4 == 0:
                last = await self.bot.say("There are still {} messages. "
                                          "Type `more` to continue."
                                          "".format(len(result) - (i+1)))
                msg = await self.bot.wait_for_message(author=author,
                                                      channel=channel,
                                                      check=check,
                                                      timeout=10)
                if msg is None:
                    try:
                        await self.bot.delete_message(last)
                    except:
                        pass
                    finally:
                        break
            await self.bot.say(box(page, lang="py"))

def setup(bot):
    bot.add_cog(Loader(bot))
