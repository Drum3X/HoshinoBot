#nextcord modules
import nextcord
from nextcord.ext import commands, menus

#python modules
from typing import List, Tuple

#import menus
from menus import InteractionCheckButtonMenuPages   
from .menus import HelpListPageSource   

class HelpCommand(commands.MinimalHelpCommand):  
    def __init__(self):
        super().__init__(
            command_attrs = {
                "help": "<category/command>", 
                "description": ""
            }
        )
  
    async def command_not_found(self, string):
        return f"{string} not found."
  
    async def send_error_message(self, err):
        raise commands.CommandError(err)
        
    async def send_bot_help(self, mapping: dict):             
        fields = []
        for cog, commands in mapping.items():  
            name = "No Category" if cog is None else cog.qualified_name
            filtered_commands = await self.filter_commands(commands, sort = True)   
            
            if filtered_commands:
                commands = "\n".join(f"{c.name}" for c in filtered_commands)
                fields.append((name.capitalize(), commands, False)) 
        
        pages = InteractionCheckButtonMenuPages(
            ctx = self.context, 
            source = HelpListPageSource(fields, "Bot Commands", self.cog.bot),
            clear_buttons_after = True, 
            timeout = self.cog.bot.pagination_timeout
        )
        await pages.start(self.context)
                                                  
    async def send_cog_help(self, cog: commands.Cog):        
        fields = []       
        filtered_commands = await self.filter_commands(cog.get_commands(), sort = True)
        
        for command in filtered_commands:
            fields.append((
                f"{command.qualified_name} {command.help or command.signature}",                
                command.description or "undefined",
                False
            ))
            
        pages = InteractionCheckButtonMenuPages(
            ctx = self.context, 
            source = HelpListPageSource(fields, f"{cog.qualified_name.capitalize()} Commands", self.cog.bot),
            clear_buttons_after = True, 
            timeout = self.cog.bot.pagination_timeout
        )
        await pages.start(self.context)  
        
    async def send_group_help(self, group):
        fields = []       
        filtered_commands = await self.filter_commands(group.commands, sort = True)
        
        for command in filtered_commands:
            fields.append((
                f"{command.qualified_name} {command.help or command.signature}",                
                command.description or "undefined",
                False
            ))
            
        pages = InteractionCheckButtonMenuPages(
            ctx = self.context, 
            source = HelpListPageSource(fields, f"{group.qualified_name}", self.cog.bot),
            clear_buttons_after = True, 
            timeout = self.cog.bot.pagination_timeout
        )
        await pages.start(self.context)  

    async def send_command_help(self, command):
        await self.cog.bot.send_embed(ctx = self.context, title = f"{command.qualified_name} {command.help or command.signature}", description = command.description or "undefined")
    
class Help(commands.Cog, name = "help"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.original_help_command = bot.help_command
        bot.help_command = HelpCommand()      
        bot.help_command.cog = self                        

    def cog_unload(self):
        self.bot.help_command = self.original_help_command

def setup(bot):
    bot.add_cog(Help(bot))      