import discord, json, asyncio, random
from discord.ext import commands
from discord.utils import get
from library import funcs, roles
import datetime

bot = commands.Bot(command_prefix='c?', intents = discord.Intents.all())

@bot.event
async def on_ready():
	print('started.')
	await bot.change_presence(status = discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Traders setup their TradeShops"))

async def check(ctx):
	with open("library/bl.json" , "r") as f:
		bl = json.load(f)
	if ctx.author.id in bl['users'] or ctx.channel.id not in bl['channels']:
		if ctx.author.guild_permissions.manage_guild == True:
			return True
		return False
	else:
		return True

bot.add_check(check)

bot.load_extension('cogs.shop')
bot.load_extension('cogs.post')
bot.load_extension('cogs.admin')

bot.remove_command('help')

@bot.command(name='help')
async def help(ctx, categ=None):
	if not categ or categ == 'all':
		embed=discord.Embed(title='ghi', description = 'Advanced and highly customizable TradeShops with pings.', color = discord.Color.random())
		embed.add_field(name='Customizing Your Shop', value = '`c?shop`\n**Aliases:** `profile`\n**Subcommands:** `view`, `addline`, `removeline`, `title`, `about`, `insert`, `reset`\nUse `c?shop add <line>` to add a line to your shop.\nE.g. `c?shop add selling pink phallics for 10 coins per`, it will auto detect whether to add to your `selling` or `buying` shop, make sure to use the words.\nUse `c?help shop` for a more detailed help.', inline=False)
		embed.add_field(name='Post', value='`c?post`\n**Aliases:** `p, send`\n**SubCommands:** `selling`, `buying`\n**Flags to Use:** `--channel #channel --pings ping1,ping2,ping3`\nE.g. `c?post selling --channel #offer-selling --pings exotic,normie`\nUse `c?pings` for a list of pings.', inline=False)
		embed.add_field(name='View', value='View another users shop. :: `c?view <user>`')
	elif categ == 'post':
		embed=discord.Embed(title='ghi', description = 'Advanced and highly customizable TradeShops with pings.', color = discord.Color.random())
		embed.add_field(name='Post', value='`c?post`\n**Aliases:** `p, send`\n**SubCommands:** `selling`, `buying`\n**Flags to Use:** `--channel #channel --pings ping1,ping2,ping3`\nE.g. `c?post selling --channel #offer-selling --pings exotic,normie`\nUse `c?pings` for a list of pings.')
	elif categ == 'shop':
		embed=discord.Embed(title='ghi', description = 'Advanced and highly customizable TradeShops with pings.', color = discord.Color.random())
		embed.add_field(name='Customizing Your Shop', value = '`c?shop`\n**Aliases:** `profile`\n**Limitations:** `50 characters per line`, `5 lines per shop`.\n**Subcommands:** `view`, `addline`, `removeline`, `title`, `about`, `insert`, `reset`', inline=False)
		embed.add_field(name='Syntaxes', value = '**add/remove**: `c?shop add buying pepet for 69k`, `c?shop remove <index>` :: Adds or removes a line from your shop.\n**Insert:** `c?shop insert <line number> <line>` :: Inserts a line with specified index.\nE.g. `c?shop insert 3 Buying Pepet for 69k`\n**Title/about**: `c?shop title/about <info>` :: Changed the title or about of your shop.\n**Reset**: `c?shop reset` :: Resets your shop.')
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
	embed.add_field(name='Selling Pings', value = sfinal, inline=False)
	embed.add_field(name='Usage Example', value = '```c?post buying --channel #offer-selling --pings exotic,normie,boxes```')
	await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		error_list = ['Woah, slow down there Sheriff!','Too fast for me, let me breath!','Spamming isn\'t cool!','Im too lazy!','Later, Aligator!','Take it slow there buddy!']
		error_random = random.choice(error_list)
		timez = int("{:.0f}")
		if timez > 60:
			timez = float(timez) / 60
			timez = round(timez)
			comment = f"**{timez}** minute(s)!"
		if timez > 3600:
			timez = float(timez) / 3600
			timez = round(timez)
			comment = f"**{timez}** hour(s)!"
		if timez > 86400:
			timez = float(timez) / 86400
			timez = round(timez)
			comment = f"**{timez}** day(s)!"
		error_embed = discord.Embed(title = f"{error_random}", description = f"You're going too fast!\nThis Command is on Cooldown!\nWait {comment}".format(error.retry_after), color = discord.Color.random())
		error_embed.set_footer(text = "» Use `c?shop` to setup your TradeShop!")
		return await ctx.send(embed = error_embed)
	elif isinstance(error, commands.CheckFailure):
		return
	else:
		raise error
		return await ctx.send(error)


bot.run('ODUwNjI0MDQ1MTkxMDA0MTYw.YLsbYA.LBigUAmdCXaVT_Fq7O9QL1meniE')