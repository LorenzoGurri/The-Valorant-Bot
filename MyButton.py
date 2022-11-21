import discord 
from discord.ui import Button, View
import clipboard 

# Custon Discrod Button Class
class MyButton(Button):
	# Initialize
	def __init__(self, teamName, roster):
		super().__init__(label = teamName, style = discord.ButtonStyle.primary)
		self.roster = roster
	# Callback Function
	async def callback(self, interaction):
		msg = discord.Embed(
			title = "Players of " + self.label,
			color = 0x0000FF
		)
		crosshairView = View()
		for player in self.roster:
			msg.add_field(name = player["name"], value = player["code"], inline = False)
			# Creating Player Button with example crosshair as emoji
			crossButton = PlayerButton(player["name"], player["code"], player["image"])
			crosshairView.add_item(crossButton)

		await interaction.response.send_message(embed = msg, view = crosshairView)
		
# Custon Player Button to copy their crosshair code to clip board
class PlayerButton(Button):
	# Initialize
	def __init__(self, player_name, player_code, image):
		super().__init__(label = player_name, style = discord.ButtonStyle.grey, emoji = image)
		self.code = player_code

	# Callback Function
	async def callback(self, interaction):
		clipboard.copy(self.code)
		msg = discord.Embed(title = "Copied to Clipboard!")
		await interaction.response.send_message(embed = msg)

		