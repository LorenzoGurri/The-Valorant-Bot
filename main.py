# IMPORTS
from audioop import cross
import discord
import os
import requests
from dotenv import load_dotenv
from discord.ui import Button, View
import json

#MongoDB stuff
import pymongo
from pymongo import MongoClient

# MyButton Class 
import MyButton
# Class stuff
import Agent
import Player

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
lineupsCollection = db["Lineups"]
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
	DiscordIDquery = { "Discord_id": msg.author.id }
	if (collection.count_documents(DiscordIDquery) == 0):
		print("msg: ", msg)
		Valusername = msg.content[13:] #Get rid of the !tvb connect part 
		ValIDQuery =  {"Valorant_ID": Valusername}
		if(collection.count_documents(ValIDQuery) != 0):
			message.title = "Connection Failed"
			message.description = 'Someone already claimed your account!!!'
		else:
			print("Val username: ", Valusername)
			print("Discord Name: ", msg.author)
			post = {"Discord_id": msg.author.id, "Discord_name": msg.author.name, "Valorant_ID": Valusername}
			collection.insert_one(post)
			message.title = "Connection Success!"
			message.description = 'Discord Name: ' + msg.author.name + '\nValorant account: ' + Valusername
	else:
		message.title = "Connection Failed"
		message.description = "User already in DATABASE!"
	await channel.send(embed=message)

#DISCONNECT: Users can disconnect a Valorant account from their Discord account
async def disconnect(msg, channel):
	message = discord.Embed(
		title = "Disconnect Account",
		description = "TODO: Set up connecting account",
		color = 0x0000FF
	)
	DiscordIDquery = { "Discord_id": msg.author.id }
	if (collection.count_documents(DiscordIDquery) == 0):
		message.title = "Disconnection Failed!"
		message.description = 'You were never connected in the first place!'
	else:
		collection.delete_one(DiscordIDquery)
		message.title = "Disconnection Success!"
		message.description = "Deleted " + msg.author.name + " from the database!" 
	await channel.send(embed=message) 

#STATS: Users will be able to see important stats related to their Valorant Account
async def stats(msg, channel, author):
	#Error checking
	if len(msg) < 3:
		await channel.send("**USAGE**: \n!tvb stats [ap,br,eu,kr,latam,na] [username#TAG]\n!tvb stats [ap,br,eu,kr,latam,na]")
		return

	region = msg[2]
	if len(msg) == 3:
		DiscordIDquery = { "Discord_id": author.id }
		user = collection.find_one(DiscordIDquery)
		if user != None:
			username = user['Valorant_ID'].replace(" ", "").split("#")
		else:
			await channel.send("**ERROR**: {} not in database\nUse !tvb connect [username#TAG]".format(author))
			return
	else:
		username = ''.join(msg[3:]).split("#")

	#Error checking
	if len(username) != 2:
		await channel.send("**ERROR**: Incorrect username#TAG format")
		return

	#API call for basic user info
	response = requests.get(api_link + "v1/mmr/{}/{}/{}".format(region, username[0], username[1]))
	#Error checking
	if response.status_code != 200:
		await channel.send("**ERROR**: Error with API response\nStatus Code: {}".format(response.status_code))
		return
	player = Player.Player(response.json()['data'])

	#API call for matches
	response = requests.get(api_link + "v3/matches/{}/{}/{}?filter=competitive".format(region, player.getUsername(), player.getTag()))
	#Error checking
	if response.status_code != 200:
		await channel.send("**ERROR**: Error with API response\nStatus Code: {}".format(response.status_code))
		return
	player.parseStats(response.json()['data'])

	#Start of output
	output = discord.Embed(
		title = "{}'s Statistics".format(username[0]),
		color = discord.Color.blue()		
	)
	output.set_thumbnail (
		url=player.getImage()
	)
	#Rank and RR
	output.add_field(
		name=player.getRank(),
		value="{}/100".format(player.getRR()),
		inline=True
	)
	output.add_field(
		name="RR Change",
		value="{}".format(player.getRRChange()),
		inline=False
	)
	#Last 5 Games
	output.add_field(
		name="K/D",
		value= "{:.2f}".format(player.getKD()),
		inline=True
	)
	output.add_field(
		name="ACS",
		value= "{:.0f}".format(player.getACS()),
		inline=True
	)
	output.add_field(
		name="Headshot %",
		value= "{:.1f}%".format(player.getHeadshot()),
		inline=True
	)


	await channel.send(embed=output)

#LINEUPS: Users will be able to search for useful lineups
async def lineups(msg, channel):

	if len(msg) != 7 :
		await channel.send("**USAGE**: !tvb lineups <MAP> <SITE> <ATTACK?> <START> <AGENT> ")
		return
	Map = msg[2].lower()
	Site = msg[3].lower()
	Type =  msg[4].lower()
	Start = msg[5].lower()
	Agent = msg[6].lower()
	print("Map:", Map, "Site:", Site, "Type:", Type, "Start:", Start,  "Agent:", Agent)
	DiscordIDquery = {"Map": Map, "Site": Site, "Type": Type, "Start": Start, "Agent": Agent}
	lineups = lineupsCollection.find_one(DiscordIDquery)
	if lineups != None:
		await channel.send(lineups["Video"])
	else:
		print("Failed:(")
		await channel.send("**ERROR**: no lineups for those requirements!!!")
	return
	#await channel.send(embed=msg)

#AGENTS: Users will be able to see useful information about Agents
async def agents(msg, channel):
	if len(msg) == 2:
		msg = discord.Embed(
			title = "Available Agents",
			description = "Astra, Breach, Brimstone, Chmaber, Cypher, Fade, Harbor, Jett, KAY/O, Killjoy, Neon, Omen, Pheonix, Raze, Reyna, Sage, Skye, Sova, Viper, Yoru",
			color = 0x0000FF
		)
		await channel.send(embed=msg)
		return

	if len(msg) != 3:
		await channel.send("**USAGE**: !tvb agents [agent_name]")
		return
	else:
		agentName = msg[2]
		path = "agents/"+agentName.lower()+".json"
		if agentName.lower() == "kay/o":
			path = "agents/kayo.json"
		try:
			with open(path, 'r') as f:
				data = json.load(f)
		except:
			await channel.send("Invalid Agent Name")
			return

		agent = Agent.Agent(data)
		name = agent.printName()
		role = agent.printRole()
		description = agent.printDescription()
		image = agent.printImage()
		abilities = agent.printAbilities()

		output = discord.Embed(
			title = "Agent: {} ({})".format(name,role),
			color = discord.Color.blue()		
		)


		output.add_field(
			name="Description",
			value=description
		)
		for ability in abilities:
			icon = ability['displayIcon']
			slot = ability['slot']
			if slot == 'Ultimate':
				output.add_field(
					name="Ability: " + ability['name'] + " (" + slot+")",
					value=ability['description'] + "\n*"+ str(ability['cost']) + " Points*",
					inline=False
				)
			elif slot == 'Passive':
				output.add_field(
					name="Ability: " + ability['name'] + " (" + slot+")",
					value=ability['description'],
					inline=False
				)
			elif ability['cost'] == 'null':
				output.add_field(
					name="Ability: " + ability['name'] + " (" + slot+")",
					value=ability['description'] + "\n*Cost: Free*",
					inline=False
				)
			else:
				output.add_field(
					name="Ability: " + ability['name'] + " (" + slot+")",
					value=ability['description'] + "\n*Cost: " + str(ability['cost']) + " credits*",
					inline=False
				)
		output.set_thumbnail(
			url=image
		)
		await channel.send(embed=output)


#FEEDBACK: Users will be sent a link to a feedback survey
async def feedback(msg, channel):
	msg = discord.Embed(
		title = "Feedback",
		description = "Please leave some feedback!\nhttps://forms.gle/hcKCUBtCyd1Zcn2Z8",
		color = 0x0000FF
	)
	await channel.send(embed=msg)

#CROSSHAIRS: Users will be able to search through various crosshairs
async def crosshairs(msg, channel):
	if len(msg) != 3:
		await channel.send("**USAGE**: !tvb crosshairs [pro / fun]")
		return
	else:
		view = View()
		typing = msg[2]
		if (typing.lower() == "pro"):
			path = "crosshairs/proCrosshairs.json"
			
			with open(path, "r") as f:
				data = json.load(f)

			allTheTeams = list()
			for team_dict in data["Teams"]:
				allTheTeams.append(team_dict)
				
				teamButton = MyButton.MyButton(team_dict["name"], team_dict["Players"])
				view.add_item(teamButton)

			await channel.send("Professional Valorant Teams", view = view)

		elif (typing.lower().startswith("fun")):
			await channel.send("Work in progess")

#HELP: Users will be able top see what commands we offer
async def help(msg, channel, message):
	print("MSG:",msg, "CHANNEL:",channel)
	msg = discord.Embed(
		title = "Help",
		description = "Functions allowed for The Valorant Bot",
		color = 0xFF5733
	)
	msg.add_field(
		name = "Connect (complete)",
		value = "!tvb connect [username#TAG]", 
		inline = False
		)
	msg.add_field(
		name = "Disconnect (complete)",
		value = "!tvb disconnect", 
		inline = False
		)
	msg.add_field(
		name = "Stats (complete)", 
		value = "!tvb stats [region] [username#TAG]\n!tvb stats [ap,br,eu,kr,latam,na]",
		inline = False
		)
	msg.add_field(
		name = "Lineups",
		value = "!tvb lineups",
		inline = False
		)
	msg.add_field(
		name = "Agents", 
		value = "!tvb agents [Agent Name]",
		inline = False
		)
	msg.add_field(
		name = "Feedback (complete)",
		value = "!tvb feedback",
		inline = False
		)
	msg.add_field(
		name = "Help (complete)",
		value = "You already used this command to see this??? \n but ... !tvb help", 
		inline = False
		)
	msg.set_footer(
		text = "Information Requested by: {}".format(message.author.display_name)
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
			elif msg[1] == "disconnect":
				await disconnect(message, message.channel)	
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
				await help(msg, message.channel, message)
			else:
				await message.channel.send("**ERROR**: Command not found!")
		else:
			await message.channel.send("**USAGE**: !tvb [command]")
	# Sends Webex Link for are Wednesday Meetings 
	elif message.content.startswith("Meeting") or message.content.startswith("meet"):
		await message.channel.send("https://rensselaer.webex.com/meet/toftl")
		

	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
	# if message.content == "hello":
	# 	# SENDS BACK A MESSAGE TO THE CHANNEL.
	# 	print("In hello")
	# 	await message.channel.send("hey dirtbag")
	# elif message.content.startswith("I'm"):
	# 	msg = message.content.split()[1]
	# 	await message.channel.send("Hi " + msg + ", I'm dad!")
	# elif message.content == "!tvb Sova Ascent B":
	# 	await message.channel.send(file=discord.File('lineups/sova_ascent_b.gif'))
	# print("hello")
	# print("message contnet: ")
	# print(message.content)
	# print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
	
# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)