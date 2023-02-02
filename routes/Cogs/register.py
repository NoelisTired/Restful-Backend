import discord, json, time, requests, datetime, hashlib, asyncio, random, string, base64
from discord.ext import commands

class RegisterCog(commands.Cog, name="register command"):
    def __init__(self, bot:commands.bot):
        self.bot = bot
        self.conf = json.load(open('./conf.json'))
        self.bot_start_time = time.time()
    def getKey(self) -> str:
        return hashlib.sha256(base64.b64encode(datetime.datetime.now().strftime("%Y%m%d").encode())).hexdigest()[::-1][::-2]+"END+aHR0cHM6Ly95b3V0dS5iZS9pNjFHLXN1TFZkOD90PTYw"
    @commands.command(name = "register",
					usage="<username>",
					description = "Adds you to the database",
                    aliases = ['apply', 'reg', 'signup'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def register(self, ctx, username: str) -> None:
        await ctx.message.delete()
        try:
            embed = discord.Embed(title=f"Account Registration [{username}]", description="Please enter your Password", color=discord.Color.blue())
            embed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
            sentEmbed = discord.Embed(title="Account Registration", description="Please check your dms", color=discord.Color.blue())
            sentEmbed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
            errorEmbed = discord.Embed(title="❌ Error", description="Please open your dms and retry", color=discord.Color.red())
            errorEmbed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
            if ctx.channel != ctx.author.dm_channel: await ctx.author.send(embed=embed); await ctx.send(embed=sentEmbed)
        except discord.Forbidden: await ctx.send(embed=errorEmbed); return
        try:
            password = await self.bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author and m.channel == ctx.author.dm_channel,
                timeout=60.0,
            )
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="❌ Error",
                description="You took too long to respond",
                color=discord.Color.red(),
            )
            embed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
            await ctx.author.send(embed=embed, delete_after=300)
            return
        r = requests.get(f"http://{self.conf['Api']['Host']}:{self.conf['Api']['Port']}/api/v1/register", headers={"User-Agent": "NoelP X - Python Requests","X-Eric-Cartman": self.getKey(),"username": username,"password": password.content, "discord": str(ctx.author.id)}).json()
        if r['Message'] == "User already exists":
            embed = discord.Embed(
                title="❌ Error",
                description="Username or Discord already registered",
                color=discord.Color.red(),
            )
            embed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
            await ctx.author.send(embed=embed, delete_after=10)
            return
        elif "Successfully" in r["Message"]:
            embed = discord.Embed(title="Account Registration", description="✅ Your account has successfully been registered", color=discord.Color.green())
            embed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
            await ctx.author.send(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(RegisterCog(bot))