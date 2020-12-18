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
    os.chdir("C:/Users/Lynn/Desktop/Server")
    process = subprocess.Popen(
        "startup.bat", shell=True, stdin=subprocess.PIPE)

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


##
##
##process_id = 0
# def on_message(message):
# if message.content == "/start":
##
##        process_id = start()
# if process_id > 0 && process_id not == False:
# return true
# else:
# return false
# elif message.content == "/stop":
##       result = stop(process_id)
# else:
# return "Server isn't started yet"
##
# def start():
# Start procedures
# return sb.process_id();
##
##
# def stop(process_id):
# Send stop command to process using the process id
# if not serverRunning():
##        process_id = 0
# return true
# else:
##        print("ERROR ERROR SERVER IS NOT RESPONDING")
# return false
##
