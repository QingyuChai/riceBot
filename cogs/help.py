import discord
import datetime
import collections

from __main__ import send_cmd_help
from discord.ext import commands

class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', pass_context=True, pm=False)
    async def _help(self, ctx, command = None):
        if not command:
            await self.bot.say("Here you go!".format(ctx.message.author.mention))
            msg = "**Command list:**"
            color = 0x002B36

            em=discord.Embed(description=msg, color=color)

        #await self.bot.say("Hello.")
        #await self.bot.say(coms)
            final_coms = {}
            com_groups = []
            for com in self.bot.commands:
                try:
                    if self.bot.commands[com].module.__name__ not in com_groups:
                        com_groups.append(self.bot.commands[com].module.__name__)
                    else:
                        continue
                except Exception as e:
                        print(e)
                        print(datetime.datetime.now())
                        continue
            com_groups.sort()
            alias = []
            #print(com_groups)
            for com_group in com_groups:
                commands = []
                for com in self.bot.commands:
                    if com_group == self.bot.commands[com].module.__name__:
                    #print("PLS WURK")
                        #if self.bot.commands[com].aliases == alias:
                        commands.append(com)
                final_coms[com_group] = commands

            #print(commands)
        #print(final_coms)

            final_coms = collections.OrderedDict(sorted(final_coms.items()))
            #print(final_coms)

            for group in final_coms:
                #width = len(max(words, key=len))
                msg = ""
                final_coms[group].sort()
                count = 0
                for com in final_coms[group]:
                #drugs = self.bot.commands[com].help
                #if not drugs:
                    #drugs = "No description available."
                #msg += '```md\n'
                    if count == 0:
                        msg += '`{}`'.format(com)
                    else:
                        msg += '~`{}`'.format(com)
                    count += 1
                #msg += '```'
                #msg += '    {}\n'.format(str(drugs))
                cog_name = group.replace("cogs.", "").title()
                cog =  "```\n"
                cog += cog_name
                cog += "\n```"
                em.add_field(name=cog, value=msg, inline=False)

            em.set_footer(text="riceBot")
            await self.bot.say(embed=em)
            await self.bot.say("riceBot - bot.discord.io/riceBot\n"
                               "A proud *variant* of Red - DiscordBot")
        else:
            asd = """msg = "**Command Help:**"
            color = 0x002B36

            em=discord.Embed(description=msg, color=color)
            try:
                commie =  "```\n"
                commie += command
                commie += "\n```"
                info = self.bot.commands[command].help
                em.add_field(name=commie, value=info, inline=False)
                em.set_footer(text="riceBot")
                await self.bot.say(embed=em)
            except Exception as e:
                print(e)
                await self.bot.say("Couldn't find command! Try again.")
            """
            await send_cmd_help(ctx, command)

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
