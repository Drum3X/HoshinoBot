#discord modules
import discord
from discord.ext import commands, tasks

#python modules
from platform import python_version, system, release
from asyncio import sleep
from json import load

#import utils
from utils import color, style

class Events(commands.Cog, name = "events"):
    def __init__(self, bot):
        self.bot = bot
        
    @tasks.loop()
    async def activity(self):       
        with open("settings.json") as file:
            data = load(file)            
   
        for activity in data.get("status"):
            await self.bot.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.playing, name = activity.get("status")))
            await sleep(activity.get("time", 60.0))
            
    @commands.Cog.listener()
    async def on_ready(self):
        self.activity.start()

def setup(bot):
    bot.add_cog(Events(bot))  
