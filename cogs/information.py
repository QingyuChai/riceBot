import discord
import datetime
import time

from discord.ext import commands

class Information:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def banlist(self, ctx):
        server = ctx.message.server
        try:
            bans = await self.bot.get_bans(server)
            msg = "```asciidoc\n"
            msg += "List of users on this server who have been banned:\n\n"
            count = 1
            for ban in bans:
                msg += "{:<5} - {}\n".format(count, ban)
                count += 1
            msg += '\n```'
            await self.bot.say(msg)
        except discord.errors.Forbidden:
            await self.bot.say("Sorry, I do not have the `ban_members` permission!")
        except:
            await self.bot.say("Nobody was banned here.")
    @commands.command()
    async def countservers(self):
        """
        Checks how many servers the bot is on"""
        msg = "The bot is in **"
        msg += str(len(self.bot.servers))
        msg += "** servers."
        await self.bot.say(msg)

    @commands.command()
    async def listchannels(self, server_id):
        """
        Checks what text channels are in a server"""
        server = self.bot.get_server(server_id)
        msg = "```asciidoc\n"
        # msg += "\n"
        count = 0
        for channel in server.channels:
            if channel.type == discord.ChannelType.text:
                channelname = channel.name.replace("_", "-")
                msg += "{} :: {}\n".format(channel.id, channelname)
                count += 1
        await self.bot.say("The server {} has {} text channels:".format(server.name, count))
        await self.bot.say(msg + "```")

    @commands.command()
    async def listservers(self):
        """
        Checks what servers the bot is on"""
        servers = self.bot.servers
        await self.bot.say("```asciidoc\nThe bot is in the following {} server(s):\n```".format(str(len(self.bot.servers))))
        msg = "```asciidoc\n"
        msg2 = "```asciidoc\n"
        msg3 = "```asciidoc\n"
        msg4 = "```asciidoc\n"
        # msg += "\n"

        messages = [msg, msg2, msg3, msg4]
        count = 0
        for server in servers:
            if len(server.members) < 10:
                messages[count] += "{:<1} :: 000{} users :: {}".format(server.id, len(server.members), server.name)
            elif len(server.members) < 100:
                messages[count] += "{:<1} :: 00{} users :: {}".format(server.id, len(server.members), server.name)
            elif len(server.members) < 1000:
                messages[count] += "{:<1} :: 0{} users :: {}".format(server.id, len(server.members), server.name)
            else:
                messages[count] += "{:<1} :: {} users :: {}".format(server.id, len(server.members), server.name)
            messages[count] += "\n"
            if len(messages[count]) > 1500:
                count = count + 1

        for message in messages:
            if len(message) > 30:
                await self.bot.say(message + "\n```")

    @commands.command(pass_context=True)
    async def discrim(self, ctx, discriminator):
        """
        Find users with this discriminator"""
        msg = "Users with discriminator " + discriminator
        msg += ": \n"
        for r in self.bot.get_all_members():
            if r.discriminator == discriminator:
                if r.name in msg:
                    pass
                else:
                    msg += "```\n"
                    msg += r.name
                    msg += "\n```"
        await self.bot.say(msg)

    @commands.command()
    async def countusers(self):
        """
        Checks how many users the bot is connected to"""
        msg = "The bot is connected to **"
        msg += str(len(set(self.bot.get_all_members())))
        msg += "** users."
        await self.bot.say(msg)



    @commands.command(pass_context=True, no_pm=True)
    async def userinfo(self, ctx, user : discord.Member = None):
        """Shows userinfo"""
        server = ctx.message.server
        if user == None:
            user = ctx.message.author

        if user.bot:
            is_bot = "Is a bot!"
        else:
            is_bot = "Is not a bot."

        joined_at = user.joined_at

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        name = user.name + "#" + user.discriminator
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        color = 0x032449

        em=discord.Embed(description=user.id, color=color)

        em.add_field(name="Status", value=user.game, inline=False)

        em.add_field(name="Bot", value=is_bot)
        em.add_field(name="Roles", value=roles)

        em.add_field(name="Joined Discord", value=user_created)
        em.add_field(name="Joined Server", value=user_joined)

        em.set_footer(text="riceBot")

        if user.avatar_url:
            em.set_author(name=name, url=user.avatar_url)
            em.set_thumbnail(url=user.avatar_url)
        else:
            em.set_author(name=name)

        try:
            await self.bot.say(embed=em)
        except discord.HTTPException:
            msg = ("Sorry! I don't have the **Embed Links** "
                   "permission! Please grant it to me!")
            await self.bot.say(msg)


    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        """Shows serverinfo"""
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days

        title = server.name
        created_on = server.created_at.strftime("%d %b %Y %H:%M")
        color = 0x032449
        region = str(server.region).title()
        user_count = "{}/{}".format(online, total_users)
        roles = len(server.roles)
        default_role = server.default_role

        em=discord.Embed(description=server.id, color=color)

        em.add_field(name="Region", value=region,)
        em.add_field(name="Created On", value=created_on)

        em.add_field(name="Text Channels", value=text_channels)
        em.add_field(name="Voice Channels", value=voice_channels)

        em.add_field(name="Roles", value=roles)
        em.add_field(name="Default Role", value=default_role)

        em.add_field(name="Usercount", value=user_count)
        em.add_field(name="Owner", value=server.owner)


        em.set_footer(text="riceBot")

        if server.icon_url:
            em.set_author(name=title, url=server.icon_url)
            em.set_thumbnail(url=server.icon_url)
        else:
            em.set_author(name=title)

        try:
            await self.bot.say(embed=em)
        except discord.HTTPException:
            msg = ("Sorry! I don't have the **Embed Links** "
                   "permission! Please grant it to me!")
            await self.bot.say(msg)


def setup(bot):
    bot.remove_command('userinfo')
    bot.remove_command('serverinfo')
    bot.add_cog(Information(bot))
