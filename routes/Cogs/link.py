import discord, json, MySQLdb, asyncio, hashlib
from discord.ext import commands
import time

dev = False

class LinkCog(commands.Cog, name="link command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.conf = json.load(open('./conf.json')) if not dev else json.load(open('./devconf.json'))
        self.db = MySQLdb.connect(
            host=self.conf["Database"]["Host"],
            port=self.conf["Database"]["Port"],
            user=self.conf["Database"]["Login"]["Username"],
            passwd=self.conf["Database"]["Login"]["Password"],
            db=self.conf["Database"]["Login"]["Database"]
        )
        self.cur = self.db.cursor()

    @commands.command(
        name="link",
        usage="",
        description="Link your account",
        alises=["link", "connect"],
    )
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def link(self, ctx, username: str) -> None:
        await ctx.message.delete()
        # Check if the user is already linked
        self.cur.execute(
            "SELECT * FROM users WHERE DISCORD = %s", (str(ctx.author.id),)
        )
        if self.cur.rowcount != 0:
            embed = discord.Embed(
                title="❌ Error",
                description="Your account is already linked",
                color=discord.Color.red(),
            )
            embed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
            await ctx.author.send(embed=embed, delete_after=10)
            return
        try:
            embed = discord.Embed(title="Link your account", description="Please enter your Username", color=discord.Color.blue())
            embed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
            sentEmbed = discord.Embed(title="Link your account", description="Please check your dms", color=discord.Color.blue())
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
        # Check if the user exists
        self.cur.execute(
            "SELECT * FROM users WHERE USERNAME = %s AND PASSWORD = %s",
            (username, hashlib.sha256(password.content.encode()).hexdigest()),
        )
        if self.cur.rowcount == 0:
            embed = discord.Embed(title="❌ Error", description="Account not Found", color=discord.Color.red())
            embed.add_field(name="Please check your username and password", value="If you don't have an account, please register one")
            embed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
            await ctx.author.send(embed=embed, delete_after=10)
            return
        # Link the account
        self.cur.execute("UPDATE users SET DISCORD = %s WHERE USERNAME = %s AND PASSWORD = %s", (str(ctx.author.id), username, hashlib.sha256(password.content.encode()).hexdigest()))
        self.db.commit()
        embed = discord.Embed(title="✅ Success", description=f"Your account has been linked to {username}", color=discord.Color.green())
        embed.set_footer(text=f"Sent at {time.strftime('%H:%M:%S')} | NoelP X")
        await ctx.author.send(embed=embed, delete_after=10)


async def setup(bot: commands.Bot):
    await bot.add_cog(LinkCog(bot))
