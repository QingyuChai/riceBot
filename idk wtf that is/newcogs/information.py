import discord
import datetime
import time

from discord.ext import commands

class Information:
    def __init__(self, bot):
        self.bot = bot

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
