import os
import discord
import subprocess

import psutil
from mcstatus import MinecraftServer

class Process:
    def __init__(self, Token):
        # self.process_data =
        process_data = None
        client = discord.Client()
        client.run(Token)
        server = None

    def update_process_data(self, data):
        self.process_data = data


    def start(self):
        os.chdir("C:/Users/Lynn/Desktop/Server")
        return subprocess.Popen("startup.bat", shell=True, stdin=subprocess.PIPE)

    @discord.client.event
    async def on_ready(self):
        print(f'{self.client.user} has connected to Discord!')

    @discord.client.event
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content == "/start":
            if serverRunning():
                await message.channel.send("Server is already running")
            else:
                await message.channel.send("Starting server")
                # startServer()
                os.chdir("C:/Users/Lynn/Desktop/Server")
                self.update_process_data(subprocess.Popen("startup.bat", shell=True, stdin=subprocess.PIPE))
                self.server = MinecraftServer("192.168.1.28:25565")


        elif message.content == "/stop":
            if serverRunning():
                await message.channel.send("Closing Server")
                self.process_data.write(bytes(message + "\r\n"), "ascii")
                self.update_process_data(None)
                self.server = None
            else:
                await message.channel.send("Server isn't running")

        elif message.content == "/server_status":
            if self.server != None:
                status = self.server.status(3)
                await message.channel.send(f' The minecraft server currently has {status.players} players with a latency of {status.latency} ms')

    def check_for_players(self):
        if self.server != None:
            status = self.server.status()
            return status.players
        else:
            return False

    def stop_if_players_0(self):
        players = self.check_for_players()
        if self.process_data != None and self.server != None:

            if players != False and players < 1:
                self.process_data.write(bytes("/stop \r\n"), "ascii")
                self.update_process_data(None)
                self.server = None
                return True
            else:
                return False
        else:
            return False

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
    if checkIfProcessRunning('java.exe'):
        return True
    else:
        return False


