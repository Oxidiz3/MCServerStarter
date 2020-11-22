import os
import discord
from dotenv import load_dotenv

serverStarted = False

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
#run when client is ready
async def on_ready():
	print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content == "/start":
		if(serverStarted):
			await message.channel.send("Server is running")
		else:
			await message.channel.send("Starting server")
			os.system("")
	elif message.content == "/stop":
		await message.channel.send("Closing Server")
	elif message.content == "/stats":
		await message.channel.send("There are X players on the server right now\n and the server has been live for X minutes")

	print("message received:", message.content)

client.run(TOKEN)