# IMPORTS
from audioop import cross
import discord
import os
import requests
from dotenv import load_dotenv

#MongoDB stuff
import pymongo
from pymongo import MongoClient

# Loads the .env file that resides on the same level as the script.
load_dotenv()
# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "knf")
if(DISCORD_TOKEN == "knf"):
	print("Error: Key not found!")
	exit(1)
# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = discord.Client(intents = discord.Intents.all())

#get the Databases
CONNECTION_URL = os.getenv("DB_CONNECTION", "knf")
if(CONNECTION_URL == "knf"):
	print("Error: Key not found!")
	exit(1)
cluster = MongoClient(CONNECTION_URL)

db = cluster["ValorantBot"]

collection = db["Player"]

command = "!tbv"
api_link = "https://api.henrikdev.xyz/valorant/"

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
async def connect(msg, channel):
	message = discord.Embed(
		title = "Connect Account",
		description = "TODO: Set up connecting account",
		color = 0x0000FF
	)
	#sample program of adding to the the database
	myquery = { "_id": msg.author.id }
	if (collection.count_documents(myquery) == 0):
		if "python" in str(msg.content.lower()):
			post = {"_id": msg.author.id, "score": 1}
			collection.insert_one(post)
			await msg.channel.send('accepted!')
	else:
		if "python" in str(msg.content.lower()):
			query = {"_id": msg.author.id}
			user = collection.find(query)
			for result in user:
				score = result["score"]
			score = score + 1
			collection.update_one({"_id":msg.author.id}, {"$set":{"score":score}})
			await msg.channel.send('accepted!')
		else:
			await msg.channel.send("**ERROR**: Command not found!")
	await channel.send(embed=message)

#STATS: Users will be able to see important stats related to their Valorant Account
async def stats(msg, channel, author):
	#Error checking
	if len(msg) != 4:
		await channel.send("**USAGE**: !tvb stats [ap,br,eu,kr,latam,na] [username#TAG]")
		return
	else:
		region = msg[2]
		username = msg[3].split("#")
		#Error checking
		if len(username) != 2:
			await channel.send("**ERROR**: Incorrect username#TAG format")
			return
		response = requests.get(api_link + "v1/mmr/{}/{}/{}".format(region, username[0], username[1]))
		#Error checking
		if response.status_code != 200:
			#I'm thinking we can add a function to handle error codes to print them out nicely
			await channel.send("**ERROR**: Error with API response\nStatus Code: {}".format(response.status_code))
			return

		#Start of output
		output = discord.Embed(
			title = "{}'s Statistics".format(username[0]),
			color = discord.Color.blue()		
		)
		user = response.json()['data']
		rank = user['currenttierpatched']
		image = user['images']['small']
		rr = user['ranking_in_tier']
		output.add_field(
			name=rank,
			value="{}/100".format(rr)
		)
		output.set_thumbnail (
			url=image
		)

		await channel.send(embed=output)

#LINEUPS: Users will be able to search for useful lineups
async def lineups(msg, channel):
	msg = discord.Embed(
		title = "Lineups",
		description = "TODO: Set up lineup command",
		color = 0x0000FF
	)
	await channel.send(embed=msg)

#CROSSHAIRS: Users will be able to search through various crosshairs
async def crosshairs(msg, channel):
	msg = discord.Embed(
		title = "Crosshairs",
		description = "TODO: Set up crosshairs command",
		color = 0x0000FF
	)
	await channel.send(embed=msg)

#AGENTS: Users will be able to see useful information about Agents
async def agents(msg, channel):
	msg = discord.Embed(
		title = "Agents",
		description = "TODO: Set up agents command",
		color = 0x0000FF
	)
	await channel.send(embed=msg)

#FEEDBACK: Users will be sent a link to a feedback survey
async def feedback(msg, channel):
	msg = discord.Embed(
		title = "Feedback",
		description = "Please leave some feedback!\nhttps://forms.gle/hcKCUBtCyd1Zcn2Z8",
		color = 0x0000FF
	)
	await channel.send(embed=msg)

#HELP: Users will be able top see what commands we offer
async def help(msg, channel):
	msg = discord.Embed(
		title = "help",
		description = "Tony's Job!",
		color = 0x0000FF
	)
	await channel.send(embed=msg)


# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
	# Make sure it doesn't respond to itself in it's own response
	if message.author == bot.user:
		return
    

	# Queue for the bot to listen
	if message.content.startswith("!tvb"):
		msg = message.content.split(" ")
		if len(msg) > 1:
			if msg[1] == "connect":
				await connect(message, message.channel)
				
			elif msg[1] == "stats":
				await stats(msg, message.channel, message.author)
			elif msg[1] == "lineups":
				await lineups(msg, message.channel)
			elif msg[1] == "crosshairs":
				await crosshairs(msg, message.channel)
			elif msg[1] == "agents":
				await agents(msg, message.channel)
			elif msg[1] == "feedback":
				await feedback(msg, message.channel)
			elif msg[1] == "help":
				await help(msg, message.channel)
		else:
			await message.channel.send("**USAGE**: !tvb [command]")


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
	print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
	
# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)