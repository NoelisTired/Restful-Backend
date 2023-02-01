import discord, json, time, MySQLdb, datetime, hashlib, asyncio, random, string
from discord.ext import commands

class RegisterCog(commands.Cog, name="register command"):
    def __init__(self, bot:commands.bot):
        self.bot = bot
        self.conf = json.load(open('./conf.json'))
        self.bot_start_time = time.time()
        self.db = MySQLdb.connect(
            host=self.conf["Database"]["Host"],
            port=self.conf["Database"]["Port"],
            user=self.conf["Database"]["Login"]["Username"],
            passwd=self.conf["Database"]["Login"]["Password"],
            db=self.conf["Database"]["Login"]["Database"])
        self.cur = self.db.cursor()
    def isDuplicate(self, username: str) -> bool:
        #? Checks if the user is already in the database
        #* Prepares the query and executes it, then commits the changes to the database
        query = "SELECT * FROM users WHERE USERNAME = %s"
        self.cur.execute(query, (username,))
        self.db.commit()
        return True if self.cur.rowcount else False
    @commands.command(name = "register",
					usage="<username>",
					description = "Adds you to the database",
                    aliases = ['apply', 'reg', 'signup'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def register(self, ctx, username: str) -> None:
        await ctx.message.delete()
        start = time.time()
        self.cur.execute(
            "SELECT * FROM users WHERE DISCORD = %s OR USERNAME = %s", (str(ctx.author.id), str(username),)
        )
        if self.cur.rowcount != 0:
            embed = discord.Embed(
                title="❌ Error",
                description="Username or Discord already registered",
                color=discord.Color.red(),
            )
            embed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
            await ctx.send(embed=embed, delete_after=10)
            return
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
        username, password, apikey = username,\
                                hashlib.sha256(password.content.encode()).hexdigest(),\
                                    ''.join(random.sample(string.ascii_lowercase, 18))
        query = "INSERT INTO users (ID, USERNAME, PASSWORD, EMAIL, OAUTH, DISCORD, APIKEY, ADMIN) VALUES (NULL,%s,%s,'EMPTY','EMPTY',%s,%s,0)"
        self.cur.execute(query, (username, password, str(ctx.author.id), apikey,))
        self.db.commit()
        print("%s | [Discord] - Registered user %s with discord %s" % (datetime.datetime.now().strftime("%H:%M:%S"), username, str(ctx.author.id)))
        embed = discord.Embed(title="Account Registration", description="✅ Your account has successfully been registered", color=discord.Color.green())
        embed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
        await ctx.author.send(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(RegisterCog(bot))