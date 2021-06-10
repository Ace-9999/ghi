import discord, json, asyncio, random
from discord.ext import commands
from library import funcs, roles

bot = commands.Bot(command_prefix='c?', intents = discord.Intents.all())

@bot.event
async def on_ready():
	print('started.')
	await bot.change_presence(status = discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Traders setup their TradeShops"))

@bot.command(name='shop', aliases = ['profile'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def shop(ctx, action=None, *, input=None):
	funcs.open_user(ctx.author)
	user = ctx.author
	users = funcs.get_users_data()
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
			embed.add_field(name="╭╯・Buying Shop", value=final2, inline=False)
		else:
			embed.add_field(name="╭╯・Buying Shop", value="Nothing here yet.", inline=False)
		if final1 != "":
			embed.add_field(name="╭╯・Selling Shop", value=final1)
		else:
			embed.add_field(name="╭╯・Selling Shop", value="Nothing here yet.")
		embed.set_thumbnail(url=user.avatar_url)
		await ctx.send(embed=embed)

	elif action == 'addline' or action == 'add':
		if 'selling' in input.lower():
			type = "selling"
		elif 'buying' in input.lower():
			type = "buying"
		else:
			return await ctx.send('Please include `selling` or `buying` in your line, so i can detect which shop to add to.')
		if len(users[str(user.id)][type]["lines"]) >= 5:
			return await ctx.send('You can only add upto 5 lines. Remove a line and then come back.')
		if not input:
			return await ctx.send('What line do i add???')
		users[str(user.id)][type]["lines"].append(input)
		users[str(user.id)][type]["lines"].remove('Nothing here yet.')
		funcs.dump(users)
		return await ctx.send(f'Added line **{input}** to your `{type}` Shop.')

	elif action == 'removeline' or action == 'remove':
		if not input:
			return await ctx.send('Which line do i remove???')
		if 'selling' in input.lower():
			input = input.lower().replace('selling ', '')
			type = "selling"
		elif 'buying' in input.lower():
			input = input.lower().replace('buying ', '')
			type = "buying"
		else:
			return await ctx.send('Please include `selling` or `buying` in your line, so i can detect which shop to remove from.')
		index = int(input)-1
		if len(users[str(user.id)][type]["lines"]) <= index:
			return await ctx.send(f'Idiot, line {index} doesn\'t exist.')
		rem = users[str(user.id)][type]["lines"][index]
		users[str(user.id)][type]["lines"].remove(rem)
		if users[str(user.id)][type]["lines"] == []:
			users[str(user.id)][type]["lines"].append('Nothing here yet.')
		funcs.dump(users)
		return await ctx.send(f'Removed line **{input}** from your `{type}` Shop.')

	elif action == 'title':
		if not input:
			return await ctx.send('What title do i put???')
		users[str(user.id)]["title"] = input
		funcs.dump(users)
		return await ctx.send(f'Changed your TradeShip `title` to **{input}**')

	elif action == 'about':
		if not input:
			return await ctx.send('What info do i put in about???')
		users[str(user.id)]["about"] = input
		funcs.dump(users)
		return await ctx.send(f'Changed your TradeShip `about` to **{input}**')

@bot.command(name='post', aliases = ['p', 'send'])
@commands.cooldown(1, 900, commands.BucketType.user)
async def post(ctx, type, *, flags):
	await ctx.message.delete()
	user = ctx.author
	funcs.open_user(user)
	users = funcs.get_users_data()
	flags = flags.split('--')
	if type == "selling":
		if len(flags) == 3 and users[str(user.id)]["pcool"] != 0:
			return await ctx.author.send(f'You are on Ping Cooldown. Try again in {users[str(user.id)]["pcool"]} minutes.')
		channel = flags[1]
		channel = channel.replace('channel ', '')
		if '<#' in channel:
			channelid = channel.replace('<#','').replace('>', '')
		else:
			channelid = channel
		channelid = int(channelid)
		"""if channelid != 719567940302929951 and channelid != 777379894090661918:
			return await ctx.send(f'You can\'t post selling ads in <#{channelid}>.')"""
		pings = flags[2].replace('pings ', '').split(',')
		if len(pings) > 3:
			return await ctx.send('You can use a max of 3 pings.')
		pongs = []
		for ping in pings:
			try:
				id = roles.SELLING.list[str(ping)]
			except KeyError:
				return await ctx.send('Invalid Pings. Use `c?pings`.')
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
			return await ctx.author.send('You don\'t have anything in your selling shop. Add something and come back later.')
		embed.set_thumbnail(url=user.avatar_url)
		strpongs = ""
		for pong in pongs:
			strpongs += f"{pong}, "
		embed.set_footer(text='Use `c?shop` to setup your TradeShop!')
		await channel.send(content=strpongs,embed=embed)
		users[str(user.id)]["pcool"] = 60
		funcs.dump(users)
		for i in range(60):
			users[str(user.id)]["pcool"] -= 1
			funcs.dump(users)
			await asyncio.sleep(60)

	elif type == "buying":
		if len(flags) == 3 and users[str(user.id)]["pcool"] != 0:
			return await ctx.author.send(f'You are on Ping Cooldown. Try again in {users[str(user.id)]["pcool"]} minutes.')
		channel = flags[1]
		channel = channel.replace('channel ', '')
		if '<#' in channel:
			channelid = channel.replace('<#','').replace('>', '')
		else:
			channelid = channel
		channelid = int(channelid)
		"""if channelid != 760637664088817675 and channelid != 777379894090661918:
			return await ctx.send(f'You can\'t post selling ads in <#{channelid}>.')"""
		pings = flags[2].replace('pings ', '').split(',')
		if len(pings) > 3:
			return await ctx.send('You can use a max of 3 pings.')
		pongs = []
		for ping in pings:
			try:
				id = roles.BUYING.list[str(ping)]
			except KeyError:
				return await ctx.send('Invalid Pings. Use `c?pings`.')
			role = f"<@&{id}>"
			pongs.append(role)
		channel = ctx.guild.get_channel(channelid)
		final1 = ""
		title = users[str(user.id)]["title"]
		about = users[str(user.id)]["about"]
		for line in users[str(user.id)]["buying"]["lines"]:
			final1 += f"» {line}\n"
		embed = discord.Embed(title=f"♡・{title}・⬦", description =f"⤷・{about}", color = discord.Color.random())
		print(final1)
		if final1 != "" and final1 != "» Nothing here yet.\n":
			embed.add_field(name="** **", value=f"⊰━━━━━━━━━━━━━━━⊱\n{final1}\n⊰━━━━━━━━━━━━━━━⊱")
		else:
			return await ctx.author.send('You don\'t have anything in your buying shop. Add something and come back later.')
		embed.set_thumbnail(url=user.avatar_url)
		strpongs = ""
		for pong in pongs:
			strpongs += f"{pong}, "
		embed.set_footer(text='Use `c?shop` to setup your TradeShop!')
		await channel.send(content=strpongs,embed=embed)
		if strpongs != "":
			users[str(user.id)]["pcool"] = 60
			funcs.dump(users)
			for i in range(60):
				users[str(user.id)]["pcool"] -= 1
				funcs.dump(users)
				await asyncio.sleep(60)
		else:
			return

bot.remove_command('help')

@bot.command(name='help')
async def help(ctx, categ=None):
	if not categ or categ == 'all':
		embed=discord.Embed(title='ghi', description = 'Advanced and highly customizable TradeShops with pings.', color = discord.Color.random())
		embed.add_field(name='Setting up Shop', value = '`c?shop`\n**Aliases:** `profile`\n**Subcommands:** `view`, `addline`, `removeline`, `title`, `about`\nUse `c?shop add <line>` to add a line to your shop.\nE.g. `c?shop add selling pink phallics for 10 coins per`, it will auto detect whether to add to your `selling` or `buying` shop, make sure to use the words.', inline=False)
		embed.add_field(name='Post', value='`c?post`\n**Aliases:** `p, send`\n**SubCommands:** `selling`, `buying`\n**Flags to Use:** `--channel #channel --pings ping1,ping2,ping3`\nE.g. `c?post selling --channel #offer-selling --pings exotic,normie`\nUse `c?pings` for a list of pings.')
	elif categ == 'post':
		embed=discord.Embed(title='ghi', description = 'Advanced and highly customizable TradeShops with pings.', color = discord.Color.random())
		embed.add_field(name='Post', value='`c?post`\n**Aliases:** `p, send`\n**SubCommands:** `selling`, `buying`\n**Flags to Use:** `--channel #channel --pings ping1,ping2,ping3`\nE.g. `c?post selling --channel #offer-selling --pings exotic,normie`\nUse `c?pings` for a list of pings.')
	elif categ == 'shop':
		embed=discord.Embed(title='ghi', description = 'Advanced and highly customizable TradeShops with pings.', color = discord.Color.random())
		embed.add_field(name='Setting up Shop', value = '`c?shop`\n**Aliases:** `profile`\n**Subcommands:** `view`, `addline`, `removeline`, `title`, `about`\nUse `c?shop add <line>` to add a line to your shop.\nE.g. `c?shop add selling pink phallics for 10 coins per`, it will auto detect whether to add to your `selling` or `buying` shop, make sure to use the words.', inline=False)
	else:
		embed=discord.Embed(title='ghi', description = f'Could not find command {categ}', color = discord.Color.red())
	return await ctx.send(embed=embed)

@bot.command(name='pings')
async def pings(ctx):
	bfinal = ""
	sfinal = ""
	for ping in roles.BUYING.list:
		bfinal += f"<@&{roles.BUYING.list[ping]}> :: {ping}\n"
	for ping in roles.SELLING.list:
		sfinal += f"<@&{roles.SELLING.list[ping]}> :: {ping}\n"
	embed=discord.Embed(title='ghi Ping List', description='**Ping Cooldown:** `30 minutes`\n**Maximum Pings Per Post:** `3`', color = discord.Color.random())
	embed.add_field(name='Buying Pings', value = bfinal, inline=False)
	embed.add_field(name='Selling Pings', value = sfinal)
	await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		error_list = ['Woah, slow down there Sheriff!','Too fast for me, let me breath!','Spamming isn\'t cool!','Im too lazy!','Later, Aligator!','Take it slow there buddy!']
		error_random = random.choice(error_list)
		
		error_embed = discord.Embed(title = f"{error_random}", description = "You're going too fast!\nThis Command is on Cooldown!\nWait **{:.0f} seconds** until the cooldown is over!".format(error.retry_after), color = discord.Color.random())
		error_embed.set_footer(text = "» Use `c?shop` to setup your TradeShop!")
		return await ctx.send(embed = error_embed)


bot.run('TOKEN')