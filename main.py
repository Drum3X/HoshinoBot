#nextcord modules
import nextcord
from nextcord.ext import commands

#python modules
from logging import FileHandler
from aiosqlite import connect
from os import listdir
from argparse import ArgumentParser
from datetime import datetime
from json import load
from re import match

#import database
from database import prepare_database

#import utils
from utils import Embed, color, style

#import errors
from errors import Error

style.clear_screen()        

extensions = [
    "cogs.commands.help",
    "cogs.commands.owner",
    "cogs.commands.moderation",
    "cogs.commands.anime",
    "cogs.commands.xash",
    "cogs.listeners.events",
    "cogs.listeners.errors"
]

parser = ArgumentParser(description = "nextcord Bot Args")
parser.add_argument("-t", "--test", action = "store_false", help = "for login with test bot token")
args = parser.parse_args()

with open("settings.json") as file:
    settings = load(file)
    
with open("manifest.json") as file:
    manifest = load(file)    

intents = nextcord.Intents.all()

class Bot(commands.AutoShardedBot):    
    def __init__(self):        
        super().__init__(command_prefix = settings.get("prefix"), intents = intents, activity = nextcord.Activity(name = "Loading..."), owner_ids = set(settings.get("owners")))
         
        self.project = manifest.get("project") 
        self.version = manifest.get("version")
        self.contributors = manifest.get("contributors")
        
        self.extension_files = extensions
                      
        self.test = args.test
        
        self.db = None
        
        self.pagination_timeout = settings.get("pagination_timeout")
                
        self.format = f"{color.green}{datetime.now().strftime('%H:%M:%S')}{color.reset} {style.bright}[{color.green}INFO{color.reset}]{style.reset}"
        self.info_format = f"{color.blue}{datetime.now().strftime('%H:%M:%S')}{color.reset} {style.bright}[{color.blue}INFO{color.reset}]{style.reset}"
        self.error_format = f"{color.red}{datetime.now().strftime('%H:%M:%S')}{color.reset} {style.bright}[{color.red}ERROR{color.reset}]{style.reset}"                
        
        self.embed_color = nextcord.Color.from_rgb(*settings.get("embed_color"))
        self.send_embed = Embed(self.embed_color).send_embed
        self.get_embed = Embed(self.embed_color).get_embed    
        self.get_error = lambda err: f"{type(err).__name__}: {err}"
        
        self.error = Error
        
    async def login(self, token: str):
        data = await self.http.static_login(token.strip())
        self._connection.user = nextcord.user.ClientUser(state=self._connection, data=data)

        await self.setup_hook()
   
    async def setup_hook(self):        
        self.db = await connect("database/database.db")    
        await prepare_database(self.db)
        
        if self.test:
            self.extension_files.append("cogs.commands.test")
            self.extension_files.append("cogs.listeners.test")
           
        for extension in self.extension_files:
            try:
                self.load_extension(f"{extension}.{extension.split('.')[-1]}")
                print(f"{self.info_format} {extension} loaded")
            except Exception as err:   
                if self.test:               
                    raise err 
                else:            
                    print(f"{self.error_format} {self.get_error(err)}")
                    
    async def process_commands(self, message):
        if message.author.bot:
            return

        ctx = await self.get_context(message)
        
        if ctx.command:
            async with self.db.execute("select ids from blacklist") as cursor:            
                blacklist = [user[0] for user in await cursor.fetchall()]                      
        
            if ctx.author.id in blacklist and ctx.author.id not in list(self.owner_ids):
                return await self.send_embed(ctx = ctx, title = "Blacklist", description = "You are blacklisted.") 
                
            async with self.db.execute("select maintenance from settings") as cursor:            
                maintenance = (await cursor.fetchone())[0]                   
        
            if maintenance and ctx.author.id not in list(self.owner_ids):
                return await self.send_embed(ctx = ctx, title = "Maintenance", description = f"{self.user.name} is in maintenance mode.")
                
        await self.invoke(ctx) 
        
    async def on_connect(self):
        print(f"\n{self.format} {self.user} connected")
    
if not args.test or not settings.get("testing_token"):
    token = settings.get("token")
else:
	   token = settings.get("testing_token")
	   	     
Bot().run(token, reconnect = True)
