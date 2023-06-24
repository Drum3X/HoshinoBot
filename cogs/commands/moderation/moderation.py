#nextcord modules
import nextcord
from nextcord.ext import commands

class Moderation(commands.Cog, name = "moderation"):
    def __init__(self, bot):
        self.bot = bot
          
    @commands.has_permissions(ban_members = True)
    @commands.command(
        name = "ban",
        aliases = [],
        help = "<user> <reason=undefined>"
    )
    async def ban(
        self, 
        ctx, 
        user: nextcord.Member, 
        *, reason = "undefined"
    ):        
        if user == ctx.author:
            raise self.bot.error("You can't ban yourself.")
  
        if user.id in list(self.bot.owner_ids):
            raise self.bot.error("You can't ban bot owners.")
  
        if user.top_role >= ctx.author.top_role and ctx.author.id not in list(self.bot.owner_ids):
            raise self.bot.error("You can't ban moderators.")
              
        try:
            await user.ban(reason = reason)

            fields = [
                ("Author", ctx.author, False),
                ("Banned User", user, False),
                ("Reason", reason, False)                       
            ]
            
            await self.bot.send_embed(ctx = ctx, title = "User Banned", fields = fields)  
             
        except:
            raise self.bot.error("User is not bannable.")
    
    @commands.has_permissions(kick_members = True)
    @commands.command(
        name = "kick",
        aliases = [],
        help = "<user> <reason=undefined>"
    )
    async def kick(
        self, 
        ctx, 
        user: nextcord.Member, 
        *, reason = "undefined"
    ):        
        if user == ctx.author:
            raise self.bot.error("You can't kick yourself.")
  
        if user.id in list(self.bot.owner_ids):
            raise self.bot.error("You can't kick bot owners.")
  
        if user.top_role >= ctx.author.top_role and ctx.author.id not in list(self.bot.owner_ids):
            raise self.bot.error("You can't kick moderators.")
         
        try:
            await user.kick(reason = reason)
            
            fields = [
                ("Author", ctx.author, False),
                ("Kicked User", user, False),
                ("Reason", reason, False)                       
            ]
            
            await self.bot.send_embed(ctx = ctx, title = "User Kicked", fields = fields)  
             
        except:
            raise self.bot.error("User is not kickable.")

    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(
        name = "purge",
        aliases = [],
        help = "<limit>"
    )
    async def purge(
        self, 
        ctx, 
        limit: int
    ):        
        if limit < 1:
            raise self.bot.error("Please enter a valid number.")
              
        if limit > 1000: 
            raise self.bot.error("Please enter a number less than 1000.") 
       
        await ctx.channel.purge(limit = limit)
        
        fields = [
            ("Author:", ctx.author, False),
            ("Amount:", limit, False)
        ]
        
        await self.bot.send_embed(ctx = ctx, title = "Purge Succesfully", fields = fields)        

    @commands.has_permissions(manage_channels = True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(
        name = "nuke",
        aliases = [],
        help = "<channel>"
    )
    async def nuke(
        self, 
        ctx, 
        channel: nextcord.TextChannel = None
    ):              
        if not channel:
            channel = ctx.channel
            
        new_channel = await channel.clone()
        
        await channel.delete()
        await new_channel.edit(position = channel.position, sync_permissions = True)        
                
        fields = [
            ("Author:", ctx.author, False)
        ]
        
        embed = self.bot.get_embed(title = "Nuke Succesfully", fields = fields)
        await new_channel.send(embed = embed)
        
def setup(bot):
    bot.add_cog(Moderation(bot))   