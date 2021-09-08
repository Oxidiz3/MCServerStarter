import os
import discord
import psutil
import subprocess
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

def checkIfProcessRunning(processName):
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def serverRunning():
    if(checkIfProcessRunning('java.exe')):
        return True
    else:
        return False

def startServer():
    os.chdir("/home/smecham/ForgeServer")
    process = subprocess.Popen(
        "/home/smecham/ForgeServer/start.bin", shell=True, stdin=subprocess.PIPE)

# ===Discord Events===
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "/start":
        if(serverRunning()):
            await message.channel.send("Server is already running")
        else:
            await message.channel.send("Starting server")
            startServer()
    elif message.content == "/stop":
        if(serverRunning()):
            await message.channel.send("Closing Server")
        else:
            await message.channel.send("Server isn't running")

client.run(TOKEN)

