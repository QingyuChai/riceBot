from discord.ext import commands

def is_owner():
    def predicate(ctx):
        return ctx.message.author.id == '124946832307519492'
    return commands.check(predicate)

def is_not_pvt_chan():
    def predicate(ctx):
        return not ctx.message.channel.is_private
    return commands.check(predicate)
