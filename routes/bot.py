import discord, json, os, asyncio, time, threading, MySQLdb, datetime
from discord.ext import commands

dev = False

with open("./conf.json", "r") as config: 
	data = json.load(config)
	token = data['Discord']['Token']
	prefix = data['Discord']['Prefix']
	owner_id = data['Discord']['OwnerID']

bot = commands.Bot(prefix, intents = discord.Intents.all(), owner_id = owner_id)

class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None
class checkDatabase:
	def __init__(self):
		self.conf = json.load(open('./conf.json')) if not dev else json.load(open('./devconf.json'))
		try: self.db = MySQLdb.connect(
			host=self.conf["Database"]["Host"],
			port=self.conf["Database"]["Port"],
			user=self.conf["Database"]["Login"]["Username"],
			passwd=self.conf["Database"]["Login"]["Password"],
			db=self.conf["Database"]["Login"]["Database"]
		)
		except: print("%s | [MySQL] Failed to connect to %s" % (time.strftime("%H:%M:%S"), f"{self.conf['Database']['Host']}:{self.conf['Database']['Port']}")); exit()
		finally: print("%s | [Discord] - Starting Discord Bot serving with prefix: %s" % (datetime.datetime.now().strftime("%H:%M:%S"), self.conf['Discord']['Prefix']))
# Load cogs
async def load_cogs():
	for filename in os.listdir("./routes/Cogs"):
		if filename.endswith(".py"):
			await bot.load_extension(f"routes.Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
	print("%s | [Discord] Logged in as @%s, watching over %s members" % (time.strftime("%H:%M:%S"), f"{bot.user.name}#{bot.user.discriminator}", len(bot.users)))
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))

async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)
if __name__ != "__main__":
	checkDatabase()
	asyncio.run(main())