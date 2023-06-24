#nextcord modules
import nextcord
from nextcord.ext import commands, menus

#python modules
import asyncio
import sqlite3
from textwrap import wrap
from platform import python_version, system, release

#import utils
from utils import async_eval, async_exec
from .utils import get_blacklist

#import menus
from menus import InteractionCheckButtonMenuPages, ListPageSource

#import converters
from converters import CodeblockConverter

class Owner(commands.Cog, name = "owner"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.is_owner()
    @commands.group(
        invoke_without_command = True,
        name = "load",
        aliases = [],
        help = "<extension/all>"
    )
    async def load(
        self, 
        ctx, 
        extension
    ):
        try:
            self.bot.load_extension(f"{extension}.{extension.split('.')[-1]}")
        except Exception as err:
            raise self.bot.error(self.bot.get_error(err))
            
        fields = [
            ("Extension", extension, False)
        ]
        await self.bot.send_embed(ctx = ctx, title = "Extension Loaded", fields = fields)
        
    @load.command(
        name = "all",
        aliases = [],
    )
    async def load_all(
        self, 
        ctx
    ):
        loaded_extensions = []
        errors = []
        for extension in self.bot.extension_files:
            try:
                self.bot.load_extension(f"{extension}.{extension.split('.')[-1]}")
                loaded_extensions.append(extension)
            except Exception as err:
                errors.append(self.bot.get_error(err))
                
        fields = [
            ("Loaded Extensions", "\n".join(loaded_extensions) if loaded_extensions else "nothing", False),
            ("Errors", "\n".join(errors), False) if errors else None
        ]
        await self.bot.send_embed(ctx = ctx, fields = fields)
        
    @commands.is_owner()
    @commands.group(
        invoke_without_command = True,
        name = "reload",
        aliases = [],
        help = "<extension/all>"
    )
    async def reload(
        self, 
        ctx, 
        extension
    ):
        try:
            self.bot.reload_extension(f"{extension}.{extension.split('.')[-1]}")
        except Exception as err:
            raise self.bot.error(self.bot.get_error(err))
            
        fields = [
            ("Extension", extension, False)
        ]
        await self.bot.send_embed(ctx = ctx, title = "Extension Reloaded", fields = fields)
        
    @reload.command(
        name = "all",
        aliases = [],
    )
    async def reload_all(
        self, 
        ctx
    ):
        reloaded_extensions = []
        errors = []
        for extension in self.bot.extension_files:
            try:
                self.bot.reload_extension(f"{extension}.{extension.split('.')[-1]}")
                reloaded_extensions.append(extension)
            except Exception as err:
                errors.append(self.bot.get_error(err))
                
        fields = [
            ("Reloaded Extensions", "\n".join(reloaded_extensions) if reloaded_extensions else "nothing", False),
            ("Errors", "\n".join(errors), False) if errors else None
        ]
        await self.bot.send_embed(ctx = ctx, fields = fields)
        
    @commands.is_owner()
    @commands.group(
        invoke_without_command = True,
        name = "unload",
        aliases = [],
        help = "<extension/all>"
    )
    async def unload(
        self, 
        ctx, 
        extension
    ):
        try:
            self.bot.unload_extension(f"{extension}.{extension.split('.')[-1]}")
        except Exception as err:
            raise self.bot.error(self.bot.get_error(err))
        
        fields = [
            ("Extension", extension, False)
        ]
        await self.bot.send_embed(ctx = ctx, title = "Extension Unloaded", fields = fields)
        
    @unload.command(
        name = "all",
        aliases = [],
    )
    async def unload_all(
        self, 
        ctx
    ):
        unloaded_extensions = []
        errors = []
        for extension in self.bot.extension_files:
            if extension.split('.')[-1] == "owner":
                continue
              
            try:
                self.bot.unload_extension(f"{extension}.{extension.split('.')[-1]}")
                unloaded_extensions.append(extension)
            except Exception as err:
                errors.append(self.bot.get_error(err))
                
        fields = [
            ("Unloaded Extensions", "\n".join(unloaded_extensions) if unloaded_extensions else "nothing", False),
            ("Errors", "\n".join(errors), False) if errors else None
        ]
        await self.bot.send_embed(ctx = ctx, fields = fields)
        
    @commands.is_owner()
    @commands.command(
        name = "botinfo",
        aliases = ["info"],
    )
    async def botinfo(
        self, 
        ctx
    ): 
        fields = [
            ("Python Version:", python_version(), False),
            ("Platform", f"{system()} {release()}", False),
            ("Guilds", len(self.bot.guilds), False),
            ("Ping", f"{int(self.bot.latency * 1000)}ms", False)
        ]        
            
        await self.bot.send_embed(ctx = ctx, fields = fields)
        
    @commands.is_owner()
    @commands.group(
        invoke_without_command = True,
        name = "blacklist",
        aliases = []
    )
    async def blacklist(
        self, 
        ctx
    ):                    
        blacklist = "\n".join([f"{await self.bot.fetch_user(id)}: {str(id)}" for id in await get_blacklist(self.bot)])            
                
        await self.bot.send_embed(ctx = ctx, title = "Blacklist", description	= blacklist or "nobody")	           
                                        
    @blacklist.command(
        name = "add",
        aliases = []
    )    
    async def blacklist_add(
        self, 
        ctx, 
        user: nextcord.User
    ):
        async with self.bot.db.execute(f"insert into blacklist values ({int(user.id)})") as cursor:
            await self.bot.db.commit()   
				        
        await self.bot.send_embed(ctx = ctx, title = "User Blacklisted", description = f"{user} added to blacklist.")
            
    @blacklist.command(
        name = "remove",
        aliases = ["delete"]
    )    
    async def blacklist_remove(
        self, 
        ctx, 
        user: nextcord.User
    ):
        if user.id not in await get_blacklist(self.bot):
            raise self.bot.error("User not in blacklist.")
				           
        async with self.bot.db.execute(f"delete from blacklist where ids = {user.id}") as cursor:
            await self.bot.db.commit()   
				        
        await self.bot.send_embed(ctx = ctx, title = "User Removed", description = f"{user} removed from blacklist.")
    
    @commands.is_owner()
    @commands.group(
        invoke_without_command = True,
        name = "maintenance",        
        aliases = []
    )
    async def maintenance(
        self, 
        ctx
    ): 
        async with self.bot.db.execute("select maintenance from settings") as cursor:            
            maintenance = await cursor.fetchone()                      
            
        await self.bot.send_embed(ctx = ctx, title = "Maintenance", description = f"{'on' if maintenance[0] else 'off'}") 
           
    @maintenance.command(
        name = "on",
        aliases = []
    )
    async def maintenance_on(
        self, 
        ctx
    ):                                     
        async with self.bot.db.execute("update settings set maintenance = 1") as cursor:
            await self.bot.db.commit()    
                                
        await self.bot.send_embed(ctx = ctx, title = "Maintenance", description = "Maintenance mode on.")         
        
    @maintenance.command(
        name = "off",
        aliases = []
    )
    async def maintenance_off(
        self, 
        ctx
    ):                                                   
        async with self.bot.db.execute("update settings set maintenance = 0") as cursor:
            await self.bot.db.commit()
            
        await self.bot.send_embed(ctx = ctx, title = "Maintenance", description = "Maintenance mode off.")  
        
    @commands.is_owner()
    @commands.command(
        name = "eval",
        aliases = ["e"]
    )
    async def eval(
        self, 
        ctx, 
        *, code: CodeblockConverter
    ):                                

        env = {
            "asyncio": asyncio,
            "nextcord": nextcord,
            "commands": commands,
            "bot": self.bot,
            "sql": sqlite3,
            "db": self.bot.db,
            "ctx": ctx
        }
        try:
            res = await async_eval(code, env)
        except Exception as err:
            if isinstance(err, asyncio.exceptions.TimeoutError):
                raise self.bot.error(f"Process timeout: {self.bot.get_error(err)}")
            else:
                raise self.bot.error(f"Process error: {self.bot.get_error(err)}")
            
        output = res.get("output")
        
        if res.get("error"):
            output = f"{type(output).__name__}: {output}"        
             
        embeds = []
        texts = wrap(output or "no output", 1000, replace_whitespace = False)        
        for text in texts:
            embed = self.bot.get_embed(title = "Output", description = text, code = True)
            embeds.append(embed)
            
        pages = InteractionCheckButtonMenuPages(            
            ctx = ctx, 
            source = ListPageSource(embeds),
            clear_buttons_after = True,
            timeout = self.bot.pagination_timeout
        )
        await pages.start(ctx)        
    
    @commands.is_owner()
    @commands.command(
        name = "exec",
        aliases = []
    )
    async def execute(
        self, 
        ctx, 
        *, code: CodeblockConverter
    ):   
        try:
            res = await async_exec(code) 
        except Exception as err:
            if isinstance(err, asyncio.exceptions.TimeoutError):
                raise self.bot.error(f"Process timeout: {self.bot.get_error(err)}")
            else:
                raise self.bot.error(f"Process error: {self.bot.get_error(err)}")
            
        output = res.get("output")
        
        if res.get("error"):
            output = res.get("error")                                                                                                                     
        	                       
        embeds = []
        texts = wrap(output or "no output", 1000, replace_whitespace = False)
        for text in texts:
            fields = [
                ("Code", res.get("return", "unknown"), False) if text == texts[0] else None,
                ("Output", text, False)
            ]
            embed = self.bot.get_embed(fields = fields, code = True)
            embeds.append(embed)
            
        pages = InteractionCheckButtonMenuPages(
            ctx = ctx, 
            source = ListPageSource(embeds),
            clear_buttons_after = True,
            timeout = self.bot.pagination_timeout
        )
        await pages.start(ctx)  
        
    @commands.is_owner()
    @commands.command(
        name = "say",
        aliases = []
    )
    async def say(
        self, 
        ctx, 
        *, title
    ):        
        await ctx.channel.send(title)
        
    @commands.is_owner()
    @commands.command(
        name = "spam",
        aliases = []
    )
    async def spam(
        self, 
        ctx, 
        num: int, 
        *, title
    ):
        for _ in range(num):
            await ctx.channel.send(title)     
    
    @nextcord.slash_command(guild_ids = [1117351446472564806]) 
    async def ping(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Pong!")
        
def setup(bot):
    bot.add_cog(Owner(bot))              