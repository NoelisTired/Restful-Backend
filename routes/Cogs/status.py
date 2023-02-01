import discord, json, time, requests
from discord.ext import commands

class StatusCog(commands.Cog, name="status command"):
    def __init__(self, bot:commands.bot):
        self.bot = bot
        self.conf = json.load(open('./conf.json'))
        self.bot_start_time = time.time()
    @commands.command(name = "status",
					usage="",
					description = "Displays the statusses of the bot and the api",
                    aliases = ['heartbeat', 'uptime', 'down'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def status(self, ctx):
        embed = discord.Embed(title="Status", description=f"Bot's ping: {round(self.bot.latency * 1000)}ms\nUptime: {round(time.time() - self.bot_start_time)}s", color=discord.Color.blue())
        #Makes request to api using data from conf.json and checks the delay
        r = requests.get(f"http://{self.conf['Api']['Host']}:{self.conf['Api']['Port']}", timeout=5)
        if r.status_code == 200:
            embed.add_field(name="API", value=f"API's ping: {round(r.elapsed.total_seconds() * 1000)}ms", inline=False)
        else:
            embed.add_field(name="API", value="API is down", inline=False)
        await ctx.channel.send(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(StatusCog(bot))