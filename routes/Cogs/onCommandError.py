import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, CheckFailure, CommandNotFound, NotOwner


class OnCommandErrorCog(commands.Cog, name="on command error"):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
        
	@commands.Cog.listener()
	async def on_command_error(self, ctx:commands.Context, error:commands.CommandError):
		if isinstance(error, commands.CommandOnCooldown):
			day = round(error.retry_after/86400)
			hour = round(error.retry_after/3600)
			minute = round(error.retry_after/60)
			if day > 0:
				embed = discord.Embed(title="🟥 Command on cooldown", description=f"This command has a cooldown, for {day} day(s)", color=discord.Color.red())
			elif hour > 0:
				embed = discord.Embed(title="🟥 Command on cooldown", description=f"This command has a cooldown, for {hour} hour(s)", color=discord.Color.red())
			elif minute > 0:
				embed = discord.Embed(title="🟥 Command on cooldown", description=f"This command has a cooldown, for {minute} minute(s)", color=discord.Color.red())
			else:
				embed = discord.Embed(title="🟥 Command on cooldown", description=f"This command has a cooldown, for {error.retry_after:.2f} second(s)", color=discord.Color.red())
			await ctx.send(embed=embed)
		elif isinstance(error, CommandNotFound):
			return
		elif isinstance(error, MissingPermissions):
			embed = discord.Embed(title="🟥 Missing permissions", description="You are missing the following permissions: "+", ".join(error.missing_perms), color=discord.Color.red())
			await ctx.send(embed=embed)
		elif isinstance(error, CheckFailure):
			embed = discord.Embed(title="🟥 Check failure", description="You are not allowed to use this command.", color=discord.Color.red())
			await ctx.send(embed=embed)
		elif isinstance(error, NotOwner):
			embed = discord.Embed(title="🟥 Not the bot owner", description="You are not the bot owner.", color=discord.Color.red())
			await ctx.send(embed=embed)
			return
		elif isinstance(error, commands.MissingRequiredArgument):
			embed = discord.Embed(title="🟥 Missing required argument", description=f"Missing required argument: {error.param.name}", color=discord.Color.red())
			await ctx.send(embed=embed)
			return
		else:
			print(error) #! Only for debugging
async def setup(bot:commands.Bot):
    await bot.add_cog(OnCommandErrorCog(bot))
