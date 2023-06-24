#nextcord modules
import nextcord
from nextcord.ext import commands

class Test(commands.Cog, name = "listener_test"):
    def __init__(self, bot):
        self.bot = bot
  
    @commands.Cog.listener()
    async def test(self, ctx):
        None

def setup(bot):
    bot.add_cog(Test(bot))        