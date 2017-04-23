import discord
import os
from collections import OrderedDict
from cogs.utils.dataIO import fileIO, dataIO
from cogs.utils import checks
from discord.ext import commands
from cogs.utils.paginator import Pages

class Help:
    def __init__(self, bot):
        self.bot = bot
        self.help = """General\n
**{prefix}help :** Returns this entire message.
**{prefix}invite :** Invite Tarik.
**{prefix}contact :** Contacts the owner.
**{prefix}moderation :** Shows all the moderation commands.
**{prefix}general :** Shows all the general commands.
**{prefix}economy :** Shows all the economy commands.
**{prefix}cooltext :** Shows all the cool text commands. """
        self.botinfo = """Botinfo\n
**{prefix}info :** Shows all of Tarik's information.
**{prefix}servercount :** Shows the total servers and users Tarik connected to.
**{prefix}website :** Shows Tarik's website.
**{prefix}officialdiscord :** Links Tarik's official Discord.
**{prefix}donate :** Information regarding donation.
**{prefix}donators :** Get a list of all the donators & their commands. """
        self.economy = """Economy\n
**{prefix}bank :** All the bank related things/settings.
**{prefix}payday :** Daily free credits.
**{prefix}balance :** Shows your/users current balance.
**{prefix}casino :** All the casino related things.
**{prefix}setcasino :** All the casino settings.
**{prefix}heist :** All heist related things.
**{prefix}setheist : ** All the heist settings.
**{prefix}economyset :** All the economy settings.
**{prefix}slot :** Bet your credits.
**{prefix}blackjack :** Bet your casino credits with blackjack.
**{prefix}allin :** Bet everything you have.
**{prefix}pay :** Pay a user.
**{prefix}coin :** Bet on heads or tails.
**{prefix}cups :** Pick the cup that is hiding the gold coin. Choose 1, 2, 3...
**{prefix}dice :** Roll 2, 7, 11 or 12 to win.
**{prefix}hilo :** Pick High, Low, Seven. Lo is < 7 Hi is > 7. 6x payout on 7.
**{prefix}war :** Modified War Card Game. """
        self.servermanagement2 = """Servermanagement 2\n
**{prefix}scheduler :** Makes the bot run a command. Can be repeated every x seconds. """
        self.servermanagement = """Servermanagement\n
**{prefix}autorole :** Sets a specific role to a user when they join.
**{prefix}antilink :** Removes discord links; kicks the advertiser after x times.
**{prefix}serverprefix :** Sets Tarik's server prefix.
**{prefix}buyroleset :** Sets the shop for users to buy roles using their credits.
**{prefix}setshop :** Shop configuration settings
**{prefix}p :** Commands/cogs permissions settings.
**{prefix}disable :** Disables a command.
**{prefix}disabled :** Lists all disabled commands.
**{prefix}enable :** Enables a command.
**{prefix}modlogset :** Sets the channel for activity logging.
**{prefix}modlogtoggle :** Toggles all the activity you want the bot to log.
**{prefix}welcomeset :** Sets a welcome/goodbye message. (Simple)
**{prefix}welcomer :** An advanced version of welcomeset. Can be embeded.
**{prefix}freerole :** Free roles which anyone can apply for. Mainly used for colours.
**{prefix}addcom :** Adds a custom command for the server.
**{prefix}customcommands :** Lists all the custom server commands.
**{prefix}delcom :** Deletes a custom command.
**{prefix}editcom :** Edits a custom command.
"""
        self.mod = """Moderator\n
**{prefix}ban :** Bans a user from the server.
**{prefix}softban :** Kicks a user, deleting 1 day worth of messages.
**{prefix}hackban :** Bans a user with their ID.
**{prefix}botclean :** Cleans all messages sent by bots & all it's triggers.
**{prefix}cleanup :** Cleans up messages.
**{prefix}prune :** Prunes messages, images, embeds etc..
**{prefix}editrole :** Edits role settings.
**{prefix}filter :** Filters/bans words from the server.
**{prefix}ignore :** Makes the bot ignore the server/channel.
**{prefix}unignore :** Unignores a channel/server.
**{prefix}kick :** kicks a user from the server.
**{prefix}mute :** Mutes a user from the server/channel.
**{prefix}unmute :** Unmutes a user from the server/channel.
**{prefix}modset :** Manages the server administration settings.
**{prefix}reason :** Edits a users case.
**{prefix}rename :** Changes a users nickname.
**{prefix}massmove :** Moves everyone for one channel to another.
**{prefix}move :** Moves users from a voice channel to another.
**{prefix}logs :** Logs past activity. """
        self.fun3 = """Fun 3\n
**{prefix}gardening :** Gardening commands.
"""
        self.fun2 = """Fun 2\n
**{prefix}lottery :** Server lotteries where users can earn credits!
**{prefix}setlottery :** Lottery settings.
**{prefix}buyrole :** A shop where users can buy roles using their credits.
**{prefix}trivia :** Trivia games.
**{prefix}build :** Generates fancy images.
**{prefix}rickroll :** Generates rickroll images.
**{prefix}userbar :** Generates a server-based userbar.
**{prefix}gif :** Retrieves first search result from giphy.
**{prefix}gifr :** Retrieves a random gif from a giphy search .
**{prefix}imgur :** Retrieves a picture from imgur.
**{prefix}kill :** Kill someone in a __creative__ way!
**{prefix}shop :** Shop Commands.
**{prefix}pending :** Pending shop list.
**{prefix}marry :** Marry a user.
**{prefix}divorce :** Divorce a user.
**{prefix}marryset :** Sets the channel for the marriage logs. Set no channel to disable.
**{prefix}spoiler :** Generates a spoiler GIF."""
        self.fun = """Fun\n
**{prefix}meme :** Generate a meme from a user's avatar or an image.
**{prefix}penis :** Check a user's penis length. (It's 100% accutate!)
**{prefix}3dtext :** Turns text into 3D.
**{prefix}3dtext1 :** Turns text into 3D v1.
**{prefix}3dtext2 :** Turns text into 3D v2.
**{prefix}3dtext3 :** Turns text into 3D v3.
**{prefix}3dtext4 :** Turns text into 3D v4.
**{prefix}art :** Turns text into Art.
**{prefix}ascii :** Turns text into Ascii.
**{prefix}bigtext :** Massivly enlarges text. 3-4 characters only.
**{prefix}blocktext :** Turns text into Blocks.
**{prefix}graffiti :** Turns text into Graffiti.
**{prefix}keytext :** Turns text into a keyboard.
**{prefix}matrix :** Turns text into a matrix style.
**{prefix}mirrortext :** Mirrors a text.
**{prefix}puffytext :** Turns text into a puffy writing.
**{prefix}slant :** Slants text.
**{prefix}speedtext :** Turns text into a speedy style.
**{prefix}text :** Generates an image with text on it.      """
        self.music = """Music\n
**{prefix}play :** Plays a link / searches and play.
**{prefix}song :** Info about the current song.
**{prefix}pause :** Pauses the current song, .resume to continue.
**{prefix}resume :** Resumes a paused song or playlist.
**{prefix}skip :** Skips a song, using the set threshold if the requester isn't.
**{prefix}stop :** Stops a currently playing song or playlist.
**{prefix}volume :** Sets the volume (0 - 100).
**{prefix}queue :** Shows the current queue.
**{prefix}disconnect :** Disconnects Tarik from the voice channel. """
        self.general = """General\n
**{prefix}topservers :** Shows the top 10 most popular servers that Tarik's in.
**{prefix}google :** Search anything!
**{prefix}weather :** Check the weather of any location!
**{prefix}calculate :** Calculate a sum!
**{prefix}serverinfo :** Shows information about the server.
**{prefix}userinfo :** Shows information about a user.
**{prefix}avatar :** Shows a users avatar.
**{prefix}names :** Shows the list of a users past names/nicknames.
**{prefix}stopwatch :** Starts/stops a stopwatch.
**{prefix}away :** Tell the bot if you're away or not.
**{prefix}translate :** Translates to any language.
**{prefix}roles :** Displays all the roles in the server.
**{prefix}role :** Displays all the users with a specific role and the amount.
**{prefix}nsfw :** All NSFW commands.

"""
        self.info = [self.general, self.music, self.fun, self.fun2, self.fun3,
                     self.mod, self.servermanagement, self.servermanagement2,
                     self.economy, self.botinfo, self.help]

    @commands.command(pass_context=True, name="help")
    async def _help(self, ctx, module : str = None):
        cogs = {}
        for cog in self.bot.cogs:
            cogs[cog] = []
            for com in self.bot.commands:
                if self.bot.commands[com].cog_name == cog:
                    cogs[cog].append(com)
        cogs = OrderedDict(sorted(cogs.items()))
        #msg = ""
        #p = commands.Paginator()
        #for cog in cogs:
        #    msg += "\n{}\n".format(cog)
        #    for com in cogs[cog]:
        #        desc = self.bot.commands[com].help
        #        if desc:
        #            if len(desc) > 30:
        #                desc = desc[:30] + "..."
        #        else:
        #            desc = ""
        #        msg += "{:<25} - {}\n".format(com, desc)
        #    p.add_line(msg)
        #to_send = []
        #for cog in cogs:
        #    msg = "{}\n\n".format(cog)
        #    for com in cogs[cog]:
        #        desc = self.bot.commands[com].help
        #        if desc:
        #            if len(desc) > 30:
        #                desc = desc[:30] + "..."
        #        else:
        #            desc = ""
        #        msg += "{:<25} - {}\n".format(com, desc)
        #    to_send.append(msg)

        info = [i.format(prefix=ctx.prefix) for i in self.info]
        p = Pages(self.bot, message=ctx.message, entries=info, per_page=1)
        await p.paginate()






def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
