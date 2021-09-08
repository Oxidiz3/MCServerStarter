import os
import discord
import psutil
import subprocess
from dotenv import load_dotenv

client = discord.Client()


class ServerManager:
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv("DISCORD_TOKEN")
        self.process = None

    def serverRunning(self):
        if self.checkIfProcessRunning("java.exe"):
            return True
        else:
            return False

    def startServer(self):
        os.chdir("/home/smecham/ForgeServer")
        self.process = subprocess.Popen(
            "/home/smecham/ForgeServer/start.sh",
            shell=True,
            stdin=subprocess.PIPE,
            # stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def close_server(self):
        self.process.communicate("stop")
        print("CLOSING SERVER =======================")

    def checkIfProcessRunning(self, processName):
        # Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False


server_manager = ServerManager()

# ===Discord Events===
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "/start":
        if server_manager.serverRunning():
            await message.channel.send("Server is already running")
        else:
            await message.channel.send("Starting server")
            server_manager.startServer()
    elif message.content == "/stop":
        # if server_manager.serverRunning():
        await message.channel.send("Closing Server")
        server_manager.close_server()
        # else:
        #     await message.channel.send("Server isn't running")


client.run(server_manager.TOKEN)
