#discord modules
import discord
from discord.ext import commands

class Errors(commands.Cog, name = "errors"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(
        self, 
        ctx, 
        err
    ):        
        send = self.bot.send_embed
        
        if isinstance(err, commands.NotOwner):            
            await send(ctx = ctx, title = "ERROR", description = "Only bot developer can use this command.")
                
        elif isinstance(err, commands.CommandNotFound):          
            await send(ctx = ctx, title = "ERROR", description = "Command not found.")
                
        elif isinstance(err, commands.NSFWChannelRequired):            
            await send(ctx = ctx, title = "ERROR", description = "Only available on nsfw channels.")
                
        elif isinstance(err, commands.MissingPermissions):             
            await send(ctx = ctx, title = "ERROR", description = "You do not have permission to do this command.")
                
        elif isinstance(err, commands.CommandOnCooldown): 
            await send(ctx = ctx, title = "COOLDOWN", description = f"Try again after {str(err.retry_after)[:3]} seconds.")
                
        elif isinstance(err, commands.BadArgument):    
            await send(ctx = ctx, title = "Bad Argument", description = f"Use: {ctx.prefix}{ctx.command.name} {ctx.command.help or ctx.command.signature}") 
                
        elif isinstance(err, commands.MissingRequiredArgument):  
            await send(ctx = ctx, title = "Bad Argument", description = f"Use: {ctx.prefix}{ctx.command.name} {ctx.command.help or ctx.command.signature}") 
                
        elif isinstance(err, commands.MemberNotFound):            
            await send(ctx = ctx, title = "ERROR", description = "Member not found.")
                
        elif isinstance(err, commands.BotMissingPermissions):            
            await send(ctx = ctx, title = "ERROR", description = "Bot missing permissions.")
                
        elif isinstance(err, commands.BotMissingAnyRole):            
            await send(ctx = ctx, title = "ERROR", description = "Bot missing permissions.")
                
        elif isinstance(err, commands.BotMissingRole):            
            await send(ctx = ctx, title = "ERROR", description = "Bot missing permissions.")
            
        elif isinstance(err, self.bot.error):
            await send(ctx = ctx, title = "ERROR", description = str(err))

        else:
            if self.bot.test:
                raise err
            else:                                 
                return print(f"{self.bot.error_format} {self.bot.get_error(err)}")
       
def setup(bot):
    bot.add_cog(Errors(bot))  