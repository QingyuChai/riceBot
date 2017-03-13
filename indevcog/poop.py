import discord
from discord.ext import commands
import asyncio


class Poop:
	"""leavin you in the dust!"""
	def __init__(self,bot):
		self.bot = bot

	async def on_message(self, message):
		if message.author.id != '270053110729277440':
			return
		to_del = ["Searching...","Queued.","Stopping...","Done.","Module enabled.","Module disabled.","You're now set as away.","You're now back."]
		if message.content in to_del:
			try:
				await asyncio.sleep(3)
				await self.bot.delete_message(message)
			except:
				pass

def setup(bot):
	n = Poop(bot)
	bot.add_cog(n)
