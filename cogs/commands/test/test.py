#nextcord modules
import nextcord
from nextcord.ext import commands

class Test(commands.Cog, name = "commands_test"):
    def __init__(self, bot):
        self.bot = bot
  
    @commands.is_owner()
    @commands.command(
        name = "test",
        aliases = [],
        help = ""
    )
    async def test(
        self, 
        ctx,
        *, a,
        b
    ):
        await ctx.channel.send(f"a: {a}\nb: {b}")

def setup(bot):
    bot.add_cog(Test(bot))     