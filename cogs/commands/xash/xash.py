#nextcord modules
import nextcord
from nextcord.ext import commands, menus

#python modules
from asyncio import gather
from re import search, IGNORECASE
from uuid import uuid4

#import libs
from libs import xashlib

#import converters
from converters import KeywordArgumentConverter

#import menus
from menus import InteractionCheckButtonMenuPages
from .menus import XashListPageSource

class Xash(commands.Cog, name = "xash"):
    def __init__(self, bot):
        self.bot = bot
  
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(
        name = "xash",
        aliases = [],
        help = "<gamedir=cstrike> <hostname> <ip> <port> <nat=0> <timeout=0.5>"
    )
    async def xash(
        self, 
        ctx, 
        param: commands.Greedy[KeywordArgumentConverter()]
    ):
        args = dict((x, y) for x, y in param)      
        
        try:
            game = args.get("gamedir", "valve")
            nat = int(args.get("nat", 0)) 
            timeout = float(args.get("timeout", 0.35))
        except:                 
            raise commands.BadArgument()        
   
        try:
            ms_list = [
                xashlib.Address(**{"addr": "ms.xash.su", "port": 27010}),
                xashlib.Address(**{"addr": "ms2.xash.su", "port": 27010}),
                xashlib.Address(**{"addr": "mentality.rip", "port": 27010})
            ]
            
            servers = {
                "servers": []
            }
            ip_list = await xashlib.get_servers(game, nat, ms_list[0], timeout)
            
            if ip_list:
                coros = [xashlib.query_servers(i, servers, timeout) for i in ip_list]
                await gather(*coros)
        except Exception as err:            
            raise self.bot.error("API Error")
        
        fields = [] 
        for server in servers.get("servers"):
            if args.get("hostname") and not bool(search(args.get("hostname").replace("[", "\[").replace("{", "\{").replace("(", "\(").replace(")", "\)"), server.get("hostname"), IGNORECASE)):
                continue
              
            if args.get("ip") and args.get("ip") != server.get("addr"):
                continue
              
            if args.get("port") and int(args.get("port")) != server.get("port"):
                continue

            info = [
                f"ip: {server.get('addr')}",
                f"port: {server.get('port')}",
                f"gamedir: {server.get('gamedir')}",
                f"map: {server.get('map')}",
                f"players: {server.get('players')}/{server.get('maxplayers')}",
                f"os: {server.get('os')}"
            ]
                
            field = (xashlib.remove_color_tags(server.get('hostname')), "\n".join(info), False)
            fields.append(field) 
                
        if not fields:
            raise self.bot.error("Server not found.")
         
        pages = InteractionCheckButtonMenuPages(
            ctx = ctx, 
            source = XashListPageSource(fields, self.bot),
            clear_buttons_after = True, 
            timeout = self.bot.pagination_timeout
        )
        await pages.start(ctx)
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(
        name = "xashid",
        aliases = [],
        help = ""
    )
    async def xashid(
        self, 
        ctx,         
    ):
        await self.bot.send_embed(ctx = ctx, title = "Id Generated", description = f"VALVE_XASH_{uuid4().hex}")

def setup(bot):
    bot.add_cog(Xash(bot))