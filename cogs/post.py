from discord.ext.commands import Cog, command, cooldown, BucketType
from discord.utils import get
import discord, datetime, asyncio
from library import funcs, roles

class Post(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def send_wait(self,ctx, msg):
		x=await ctx.send(msg)
		await asyncio.sleep(10)
		await x.delete()
	
	@command(name='post', aliases = ['p', 'send'])
	async def post(self,ctx, type, *, flags=None):
		if not flags:
			return await self.send_wait(ctx,'Please include channel using `c?post <type> --channel #channel`.')
		await ctx.message.delete()
		user = ctx.author
		funcs.open_user(user)
		users = funcs.get_users_data()
		if '—' in flags:
			flags = flags.split('—')
		else:
			flags = flags.split('--')
		if flags == []:
			return await self.send_wait(ctx,'Please include channel using --channel #channel.')
		if type == "selling":
			if len(flags) == 3 and users[str(user.id)]["selling"]["pcool"] != 0:
				return await self.send_wait(ctx,f'You are on Ping Cooldown. Try again in {users[str(user.id)]["pcool"]} minutes or post your ad without a ping.')
			if users[str(user.id)]["selling"]["cool"] != 0:
				col = users[str(user.id)]["selling"]["cool"]
				return await self.send_wait(ctx, f"You are on cooldown from posting selling ads! Try again in {col} minutes!")
			channel = flags[1]
			channel = channel.replace('channel ', '')
			if '<#' in channel:
				channelid = channel.replace('<#','').replace('>', '')
			else:
				channelid = channel
			try:
				channelid = int(channelid)
			except:
				return await self.send_wait(ctx, "Either the channel was not specified, or specified wrong.")
			if channelid != 719567940302929951 and channelid != 777379894090661918:
				return await self.send_wait(ctx,f'You can\'t post selling ads in <#{channelid}>.')
			try:
				pings = flags[2].replace('pings ', '').replace('ping ', '').split(',')
			except:
				pings = []
			if len(pings) > 3:
				return await self.send_wait(ctx,'You can use a max of 3 pings.')
			pongs = []
			if pings != []:
				for ping in pings:
					try:
						id = roles.SELLING.list[str(ping)]
					except KeyError:
						return await self.send_wait(ctx,'Invalid Pings. Use `c?pings`.')
					role = f"<@&{id}>"
					pongs.append(role)
			channel = ctx.guild.get_channel(channelid)
			final1 = ""
			title = users[str(user.id)]["title"]
			about = users[str(user.id)]["about"]
			for line in users[str(user.id)]["selling"]["lines"]:
				final1 += f"» {line}\n"
			embed = discord.Embed(title=f"♡・{title}・⬦", description =f"⤷・{about}", color = discord.Color.random())
			if final1 != "" and final1 != "» Nothing here yet.\n":
				embed.add_field(name="** **", value=f"⊰━━━━━━━━━━━━━━━⊱\n{final1}\n⊰━━━━━━━━━━━━━━━⊱")
			else:
				return await self.send_wait(ctx,'You don\'t have anything in your selling shop. Add something and come back later.')
			embed.set_thumbnail(url=user.avatar_url)
			strpongs = ""
			for pong in pongs:
				strpongs += f"{pong}, "
			embed.set_footer(text='Use `c?shop` to setup your TradeShop!')
			await channel.send(content=strpongs,embed=embed)
			if get(ctx.guild.roles, id=123) in ctx.author.roles:
				if strpongs != "":
					users[str(user.id)]["selling"]["pcool"] = 30
				users[str(user.id)]["selling"]["cool"] = 15
			else:
				if strpongs != "":
					users[str(user.id)]["selling"]["pcool"] = 60
				users[str(user.id)]["selling"]["cool"] = 30
			funcs.dump(users)
			for i in range(60):
				if strpongs != "":
					users[str(user.id)]["selling"]["pcool"] -= 1
				users[str(user.id)]["selling"]["cool"] -= 1
				funcs.dump(users)
				await asyncio.sleep(60)
			else:
				return

		elif type == "buying":
			if len(flags) == 3 and users[str(user.id)]["buying"]["pcool"] != 0:
				return await self.send_wait(ctx,f'You are on Ping Cooldown. Try again in {users[str(user.id)]["pcool"]} minutes or post your ad without a ping.')
			if users[str(user.id)]["buying"]["cool"] != 0:
				col = users[str(user.id)]["buying"]["cool"]
				return await self.send_wait(ctx, f"You are on cooldown from posting buying ads! Try again {col} minutes!")
			channel = flags[1]
			channel = channel.replace('channel ', '')
			if '<#' in channel:
				channelid = channel.replace('<#','').replace('>', '')
			else:
				channelid = channel
			try:
				channelid = int(channelid)
			except:
				return await self.send_wait(ctx, "Either the channel was not specified, or specified wrong.")
			if channelid != 760637664088817675 and channelid != 777379894090661918:
				return await self.send_wait(ctx,f'You can\'t post selling ads in <#{channelid}>.')
			try:
				pings = flags[2].replace('pings ', '').replace('ping ', '').split(',')
			except:
				pings = []
			if len(pings) > 3:
				return await self.send_wait(ctx,'You can use a max of 3 pings.')
			pongs = []
			if pings != []:
				for ping in pings:
					try:
						id = roles.BUYING.list[str(ping)]
					except KeyError:
						return await self.send_wait(ctx,'Invalid Pings. Use `c?pings`.')
					role = f"<@&{id}>"
					pongs.append(role)
			channel = ctx.guild.get_channel(channelid)
			final1 = ""
			title = users[str(user.id)]["title"]
			about = users[str(user.id)]["about"]
			for line in users[str(user.id)]["buying"]["lines"]:
				final1 += f"» {line}\n"
			embed = discord.Embed(title=f"♡・{title}・⬦", description =f"⤷・{about}", color = discord.Color.random())
			if final1 != "" and final1 != "» Nothing here yet.\n":
				embed.add_field(name="** **", value=f"⊰━━━━━━━━━━━━━━━⊱\n{final1}\n⊰━━━━━━━━━━━━━━━⊱")
			else:
				return await self.send_wait(ctx,'You don\'t have anything in your buying shop. Add something and come back later.')
			embed.set_thumbnail(url=user.avatar_url)
			strpongs = ""
			for pong in pongs:
				strpongs += f"{pong}, "
			embed.set_footer(text='Use `c?shop` to setup your TradeShop!')
			await channel.send(content=strpongs,embed=embed)
			if get(ctx.guild.roles, id=123) in ctx.author.roles:
				if strpongs != "":
					users[str(user.id)]["buying"]["pcool"] = 30
				users[str(user.id)]["buying"]["cool"] = 15
			else:
				if strpongs != "":
					users[str(user.id)]["buying"]["pcool"] = 60
				users[str(user.id)]["buying"]["cool"] = 30
			funcs.dump(users)
			for i in range(60):
				if strpongs != "":
					users[str(user.id)]["buying"]["pcool"] -= 1
				users[str(user.id)]["buying"]["cool"] -= 1
				funcs.dump(users)
				await asyncio.sleep(60)
			else:
				return

def setup(bot):
	bot.add_cog(Post(bot))