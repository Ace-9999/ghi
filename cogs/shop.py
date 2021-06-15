import discord, asyncio
from discord.ext.commands import Cog, command
from library import funcs, roles
from discord.utils import get

class Shopping(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def send_wait(self,ctx, msg):
		x=await ctx.send(msg)
		await asyncio.sleep(10)
		await x.delete()
	
	def rolescheck(self,ctx,user):
		role = get(ctx.guild.roles, id=850757294857781278) #replace
		role2 = get(ctx.guild.roles, id=850757324116066315) #replace
		if role in user.roles:
			return 15
		elif role2 in user.roles:
			return 10
		else:
			return 5

	@command(name='shop', aliases=['profile'])
	async def shop(self, ctx, action=None, *, input=None):
		try:
			if '@' in input:
				return await self.send_wait(ctx,'Detected Ping in input. Try again.')
		except:
			pass
		funcs.open_user(ctx.author)
		user = ctx.author
		users = funcs.get_users_data()
		pcool1 = users[str(user.id)]["selling"]["pcool"]
		pcool2 = users[str(user.id)]["buying"]["pcool"]
		cool = users[str(user.id)]["selling"]["cool"]
		cool2 = users[str(user.id)]["buying"]["cool"]
		if action == 'view' or action == None:
			final1 = ""
			final2 = ""
			title = users[str(user.id)]["title"]
			about = users[str(user.id)]["about"]
			for line in users[str(user.id)]["selling"]["lines"]:
				final1 += f"» {line}\n"
			for line in users[str(user.id)]["buying"]["lines"]:
				final2 += f"» {line}\n"
			embed = discord.Embed(title=f"♡・{title}・⬦", description =f"⤷・{about}", color = discord.Color.random())
			if final2 != "":
				embed.add_field(name="╭╯・Buying Shop", value=f"{final2}\n**Ping Cooldown:** {pcool2} minutes\n**Cooldown:** {cool2} minutes", inline=False)
			else:
				embed.add_field(name="╭╯・Buying Shop", value=f"Nothing here yet.\n**Ping Cooldown:** {pcool2} minutes\n**Cooldown:** {cool2} minutes", inline=False)
			if final1 != "":
				embed.add_field(name="╭╯・Selling Shop", value=f"{final1}\n**Ping Cooldown:** {pcool1} minutes\n**Cooldown:** {cool} minutes")
			else:
				embed.add_field(name="╭╯・Selling Shop", value=f"Nothing here yet.\n**Ping Cooldown:** {pcool1} minutes\n**Cooldown:** {cool} minutes")
			embed.set_thumbnail(url=user.avatar_url)
			await ctx.send(embed=embed)

		elif action == 'insertline' or action == 'insert':
			if not input:
				return await self.send_wait(ctx,'SyntaxError... `c?shop insert 5 buying pepet for 69k`')
			if 'selling' in input.lower():
				type = "selling"
			elif 'buying' in input.lower():
				type = "buying"
			else:
				return await self.send_wait(ctx,'Please include `selling` or `buying` in your line, so i can detect which shop to add to.')
			id1 = int(list(roles.perks.keys())[0])
			id2 = int(list(roles.perks.keys())[1])
			for role in roles.perks:
				id1 = int(role)
			if get(ctx.guild.roles, id=id1) in ctx.author.roles:
				limit = roles.perks[str(id1)]
			elif get(ctx.guild.roles, id=id2) in ctx.author.roles:
				limit = roles.perks[str(id2)]
			else:
				limit = 5
			if len(users[str(user.id)][type]["lines"]) >= limit:
				return await self.send_wait(ctx,f'You can only add upto {limit} lines. Remove a line and then come back.\nRole Limiting:\n{get(ctx.guild.roles, id=id1).name} :: {roles.perks[str(id1)]}\n{get(ctx.guild.roles, id=id2).name} :: {roles.perks[str(id2)]}')
			if len(input) > 50:
				return await self.send_wait(ctx,'You can only add upto 50 characters in one line.')
			try:
				index = int(input[0])-1
			except:
				return await self.send_wait(ctx,'Mention Index Properly... `c?shop insert 5 buying pepet for 69k`')
			final = input.replace(f"{input[0]} ", '')
			users[str(user.id)][type]["lines"].insert(index,final)
			if "Nothing here yet." in users[str(user.id)][type]["lines"]:
				users[str(user.id)][type]["lines"].remove('Nothing here yet.')
			funcs.dump(users)
			return await ctx.send()
			embed = discord.Embed(title="Success!",description=f'Inserted line **{final}** into your `{type}` Shop, as line `{int(input[0])}`.',color=discord.Color.green())
			return await ctx.send(embed=embed)

		elif action == "reset":
			if users[str(user.id)]["buying"]["cool"] != 0 or users[str(user.id)]["selling"]["cool"] !=0 or users[str(user.id)]["buying"]["pcool"] !=0 or users[str(user.id)]["selling"]["pcool"] !=0:
				return await self.send_wait(ctx,'Your cooldown is currently active, you can only reset once it reaches 0. Reset aborted.')
			del users[str(user.id)]
			funcs.dump(users)
			embed = discord.Embed(title="Success!",description=f"Reset your Shop.",color=discord.Color.green())
			return await ctx.send(embed=embed)

		elif action == 'addline' or action == 'add' or action == "+":
			if 'selling' in input.lower():
				type = "selling"
			elif 'buying' in input.lower():
				type = "buying"
			else:
				return await self.send_wait(ctx,'Please include `selling` or `buying` in your line, so i can detect which shop to add to.')
			id1 = int(list(roles.perks.keys())[0])
			id2 = int(list(roles.perks.keys())[1])
			if get(ctx.guild.roles, id=id1) in ctx.author.roles:
				limit = roles.perks[str(id1)]
			elif get(ctx.guild.roles, id=id2) in ctx.author.roles:
				limit = roles.perks[str(id2)]
			else:
				limit = 5
			if len(users[str(user.id)][type]["lines"]) >= limit:
				return await self.send_wait(ctx,f'You can only add upto {limit} lines. Remove a line and then come back.\nRole Limiting:\n{get(ctx.guild.roles, id=id1).name} :: {roles.perks[str(id1)]}\n{get(ctx.guild.roles, id=id2).name} :: {roles.perks[str(id2)]}')
			if not input:
				return await self.send_wait(ctx,'What line do i add???')
			if len(input) > 50:
				return await self.send_wait(ctx,'You can only add upto 50 characters in one line.')
			users[str(user.id)][type]["lines"].append(input)
			if "Nothing here yet." in users[str(user.id)][type]["lines"]:
				users[str(user.id)][type]["lines"].remove('Nothing here yet.')
			funcs.dump(users)
			embed = discord.Embed(title="Success!",description=f"Added line **{input}** to your `{type}` Shop.",color=discord.Color.green())
			return await ctx.send(embed=embed)

		elif action == 'removeline' or action == 'remove' or action == "-":
			if not input:
				return await self.send_wait(ctx,'Which line do i remove???')
			if 'selling' in input.lower():
				input = input.lower().replace('selling ', '')
				type = "selling"
			elif 'buying' in input.lower():
				input = input.lower().replace('buying ', '')
				type = "buying"
			else:
				return await self.send_wait(ctx,'Please include `selling` or `buying` in your line, so i can detect which shop to remove from.')
			index = int(input)-1
			if len(users[str(user.id)][type]["lines"]) <= index:
				return await ctx.send(f'Idiot, line {input} doesn\'t exist.')
			rem = users[str(user.id)][type]["lines"][index]
			users[str(user.id)][type]["lines"].remove(rem)
			if users[str(user.id)][type]["lines"] == []:
				users[str(user.id)][type]["lines"].append('Nothing here yet.')
			funcs.dump(users)
			embed = discord.Embed(title="Success!",description=f"Removed line **{input}** from your `{type}` Shop.",color=discord.Color.green())
			return await ctx.send(embed=embed)

		elif action == 'title':
			if not input:
				return await self.send_wait(ctx,'What title do i put???')
			users[str(user.id)]["title"] = input
			funcs.dump(users)
			embed = discord.Embed(title="Success!",description=f"Changed your TradeShip `title` to **{input}**",color=discord.Color.green())
			return await ctx.send(embed=embed)

		elif action == 'about':
			if not input:
				return await self.send_wait(ctx,'What info do i put in about???')
			users[str(user.id)]["about"] = input
			funcs.dump(users)
			embed = discord.Embed(title="Success!",description=f"Changed your TradeShip `about` to **{input}**",color=discord.Color.green())
			return await ctx.send(embed=embed)

	@command(name='view', aliases = ['viewshop'])
	async def viewprofile(self,ctx, user:discord.Member):
		funcs.open_user(ctx.author)
		users = funcs.get_users_data()
		final1 = ""
		final2 = ""
		title = users[str(user.id)]["title"]
		about = users[str(user.id)]["about"]
		for line in users[str(user.id)]["selling"]["lines"]:
			final1 += f"» {line}\n"
		for line in users[str(user.id)]["buying"]["lines"]:
			final2 += f"» {line}\n"
		embed = discord.Embed(title=f"♡・{title}・⬦", description =f"⤷・{about}", color = discord.Color.random())
		if final2 != "":
			embed.add_field(name="╭╯・Buying Shop", value=final2, inline=False)
		else:
			embed.add_field(name="╭╯・Buying Shop", value="Nothing here yet.", inline=False)
		if final1 != "":
			embed.add_field(name="╭╯・Selling Shop", value=final1)
		else:
			embed.add_field(name="╭╯・Selling Shop", value="Nothing here yet.")
		embed.set_thumbnail(url=user.avatar_url)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Shopping(bot))