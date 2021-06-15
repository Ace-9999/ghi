from discord.ext.commands import Cog, command, cooldown, BucketType, has_permissions
from discord.utils import get
import discord, datetime, asyncio, json
from library import funcs, roles

class Admin(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@command(name='blacklist', aliases = ['bl'])
	@has_permissions(manage_guild=True)
	async def blacklist(self, ctx, user:discord.Member):
		with open("library/bl.json", "r") as f:
			users = json.load(f)
		if user.id in users["users"]:
			return await ctx.send('User already blacklisted.')
		users["users"].append(user.id)
		with open("library/bl.json", "w") as f:
			json.dump(users,f)
		return await ctx.send('Blacklisted User.')

	@command(name='unblacklist', aliases = ['ubl', 'unbl'])
	@has_permissions(manage_guild=True)
	async def unblacklist(self, ctx, user:discord.Member):
		with open("library/bl.json", "r") as f:
			users = json.load(f)
		if user.id not in users["users"]:
			return await ctx.send('User already Unblacklisted.')
		users["users"].remove(user.id)
		with open("library/bl.json", "w") as f:
			json.dump(users,f)
		return await ctx.send('Unblacklisted User.')
	
	@command(name='toggle', aliases = ['channel'])
	@has_permissions(manage_guild=True)
	async def channel(self, ctx, channel):
		if '<#' in channel:
			channel = ctx.guild.get_channel(int(channel.replace('<#', '').replace('>', '')))
		else:
			channel = ctx.guild.get_channel(int(channel))
		with open("library/bl.json", "r") as f:
			users = json.load(f)
		if channel.id in users["channels"]:
			users["channels"].remove(channel.id)
			tog = "Removed"
		else: # where is this error? it is unable to convert channel mention into channel obj ill fix
			users["channels"].append(channel.id)
			tog = "Added"
		with open("library/bl.json", "w") as f:
			json.dump(users,f)
		return await ctx.send(f'{tog} <#{channel.id}>.')

	@command(name='settings')
	@has_permissions(manage_guild=True)
	async def settings(self, ctx):
		with open("library/bl.json", "r") as f:
			users = json.load(f)
		final = ""
		for channel in users['channels']:
			final += f"<#{channel}>\n"
		embed= discord.Embed(title='Settings :: ghI', description = 'Use `c?toggle #channel` to add/remove a channel.', color = discord.Color.random())
		embed.add_field(name='Whitelisted Channels (In which people can use commands)', value=final)
		return await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Admin(bot))