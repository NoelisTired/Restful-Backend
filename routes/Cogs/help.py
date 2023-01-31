import discord
from discord.ext import commands
from random import randint

class HelpCog(commands.Cog, name="help command"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(name='help',
                    usage="(commandName)",
                    description="Display the help message.",
                    aliases=['h', '?'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def help(self, ctx, commandName: str = None):
        if commandName:
            cmd = next((c for c in self.bot.commands if c.name == commandName.lower() or commandName.lower() in c.aliases), None)
            if cmd:
                embed = discord.Embed(title=f"{cmd.name.upper()} Command", description="", color=randint(0, 0xffffff))
                embed.add_field(name="Name", value=cmd.name, inline=False)
                embed.add_field(name="Aliases", value=", ".join(cmd.aliases) if cmd.aliases else "None", inline=False)
                embed.add_field(name="Usage", value=f"{self.bot.command_prefix}{cmd.name} {cmd.usage}" if cmd.usage else "None", inline=True)
                embed.add_field(name="Description", value=cmd.description, inline=True)
                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send("No command found!")
        else:
            embed = discord.Embed(title="Help page", description=f"{self.bot.command_prefix}help (commandName), display the help list or the help data for a specific command.", color=randint(0, 0xffffff))
            [embed.add_field(name=c.name, value=c.description, inline=True) for c in self.bot.commands]
            await ctx.channel.send(embed=embed)

async def setup(bot: commands.Bot):
    bot.remove_command("help")
    await bot.add_cog(HelpCog(bot))
