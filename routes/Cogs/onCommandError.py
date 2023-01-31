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
				await ctx.send('This command has a cooldown, for '+str(day)+ "day(s)")
			elif hour > 0:
				await ctx.send('This command has a cooldown, for '+str(hour)+ " hour(s)")
			elif minute > 0:
				await ctx.send('This command has a cooldown, for '+ str(minute)+" minute(s)")
			else:
				await ctx.send(f'This command has a cooldown, for {error.retry_after:.2f} second(s)')
		elif isinstance(error, CommandNotFound):
			return
		elif isinstance(error, MissingPermissions):
			await ctx.send("You are missing the following permissions: "+", ".join(error.missing_perms))
		elif isinstance(error, CheckFailure):
			await ctx.send("You are not allowed to use this command.")
		elif isinstance(error, NotOwner):
			await ctx.send("You are not the bot owner.")
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send(f"Missing required argument: {error.param.name}")
		else:
			await ctx.send("Unknown error, please refer to the console.")
			print(error)
async def setup(bot:commands.Bot):
    await bot.add_cog(OnCommandErrorCog(bot))
