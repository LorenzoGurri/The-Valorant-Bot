# IMPORTS
from audioop import cross
import discord
import os
from dotenv import load_dotenv

# Loads the .env file that resides on the same level as the script.
load_dotenv()
# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "knf")
if(DISCORD_TOKEN == "knf"):
	print("Error: Key not found!")
	exit(1)
# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = discord.Client(intents = discord.Intents.all())

command = "!tbv"

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
	# CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
	for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
	print("TheValorantBot is in " + str(guild_count) + " servers.")

#CONNECT: Users will be able to connect their Valorant accounts to the bot
async def connect(message):
	await(message.channel.send("Will prompt account connection"))

#STATS: Users will be able to see important stats related to their Valorant Account
async def stats(message):
	await(message.channel.send("Will print stats"))

#LINEUPS: Users will be able to search for useful lineups
async def lineups(message):
	await(message.channel.send("Will deal with lineups"))

#CROSSHAIRS: Users will be able to search through various crosshairs
async def crosshairs(message):
	await(message.channel.send("Will show crosshair options"))

#AGENTS: Users will be able to see useful information about Agents
async def agents(message):
	await(message.channel.send("Will do agent stuff"))

#FEEDBACK: Users will be sent a link to a feedback survey
async def feedback(message):
	await(message.channel.send("Please leave some feedback!\nhttps://forms.gle/hcKCUBtCyd1Zcn2Z8"))


# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
	# Make sure it doesn't respond to itself in it's own response
	if message.author == bot.user:
		return

	# Queue for the bot to listen
	if message.content.startswith("!tvb"):
		print("found command")
		msg = message.content.split(" ", 2)
		print(msg)
		if len(msg) > 1:
			if msg[1] == "connect":
				await connect(message)
			elif msg[1] == "stats":
				await stats(message)
			elif msg[1] == "lineups":
				await lineups(message)
			elif msg[1] == "crosshairs":
				await crosshairs(message)
			elif msg[1] == "agents":
				await agents(message)
			elif msg[1] == "feedback":
				await feedback(message)
			else:
				await message.channel.send("Command not found!")
		else:
			await message.channel.send("USAGE: !tvb [command]")


	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
	if message.content == "hello":
		# SENDS BACK A MESSAGE TO THE CHANNEL.
		print("In hello")
		await message.channel.send("hey dirtbag")
	elif message.content.startswith("I'm"):
		msg = message.content.split()[1]
		await message.channel.send("Hi " + msg + ", I'm dad!")
	elif message.content == "!tvb Sova Ascent B":
		await message.channel.send(file=discord.File('lineups/sova_ascent_b.gif'))
	print("hello")
	print("message contnet: ")
	print(message.content)

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)