#nextcord modules
import nextcord
from nextcord.ext import commands, menus

#python modules
from textwrap import wrap

#import libs
from libs.animelib.tracemoe import AsyncTracemoe
from libs.animelib.anilist import AsyncClient

#import menus
from menus import InteractionCheckButtonMenuPages, ListPageSource

#import converters
from converters import KeywordArgumentConverter

class Anime(commands.Cog, name = "anime"):
    def __init__(self, bot):
        self.bot = bot
        self.client = AsyncClient()
        self.tracemoe = AsyncTracemoe()    
  
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.group(
        invoke_without_command = True,
        name = "anilist",
        aliases = [],
        help = "<anime/manga/character>"
    )
    async def anilist(
        self, 
        ctx,
    ):
        raise commands.BadArgument()
        
    @anilist.command(
        name = "anime",
        aliases = [],
        help = "<search>"
    )
    async def anilist_anime(
        self,
        ctx,
        *, search,
    ):
        try:
            if search.isdigit():
                anime = await self.client.get_anime_with_id(search)
            else:
                anime = await self.client.get_anime(search)
        except Exception as err:
            raise self.bot.error("API Error.")
            
        if not anime:
            raise self.bot.error("Anime not found.")
        
        start_date = anime.start_date()
        end_date = anime.end_date()
        time = ""
        
        if any(list(start_date.values())):
            time += "start date: "
            if start_date.get("day"):
                time += str(start_date.get("day")) + "."
                
            if start_date.get("month"):
                time += str(start_date.get("month")) + "."
            
            if start_date.get("year"):
                time += str(start_date.get("year"))
        
        if any(list(end_date.values())):
            time += "\nend date: "
            if end_date.get("day"):
                time += str(end_date.get("day")) + "."
                
            if end_date.get("month"):
                time += str(end_date.get("month")) + "."
            
            if end_date.get("year"):
                time += str(end_date.get("year"))  
        
        if anime.status() == "RELEASING" and anime.next_episode():
            next_episode = anime.next_episode().get("time_until_air")
            air_time = ""
            
            if next_episode.get("days"):
                air_time += str(next_episode.get("days", "unknown")) + " days "
                
            if next_episode.get("hours"):
                air_time += str(next_episode.get("hours", "unknown")) + " hours "
                
            if next_episode.get("minutes"):
                air_time += str(next_episode.get("minutes", "unknown")) + " minutes "
                
            if next_episode.get("seconds"):
                air_time += str(next_episode.get("seconds", "unknown")) + " seconds"
            
        fields = [
            ("Id", str(anime.id()), False) if anime.id() else None,
            ("Title", anime.title("romaji"), False) if anime.title("romaji") else None,
            ("Format", anime.format().upper(), False) if anime.format() else None,
            ("Genres", ", ".join(anime.genres()), False) if anime.genres() else None,
            ("Score", anime.score(), False) if anime.score() else None,
            ("Episodes", f"{anime.episodes()} episodes", False) if anime.episodes() else None,
            ("Duration", f"{anime.duration()} minutes", False) if anime.duration() else None,
            ("Status", anime.status().replace("_", " ").lower(), False) if anime.status() else None,
            ("Time", time, False) if any(list(start_date.values())) or any(list(end_date.values())) else None,
            ("Next Episode", f"Episode {anime.next_episode().get('episode', 'unknown')} is {air_time} later", False) if anime.status() == "RELEASING" and anime.next_episode() else None
        ]

        embed = self.bot.get_embed(fields = fields)
        embed.set_image(anime.image())
        
        embeds = [embed]
        if anime.characters(): 
            fields = []                       
            for character in anime.characters()[:4]:
                fields.append((character.get("full"), f"id: {character.get('id')}\nrole: {character.get('role').lower()}\nfavourites: {character.get('favourites')}", False))
                        
            embed = self.bot.get_embed(
                title = "Characters", 
                fields = fields                 
            )
            embed.set_footer(text = "For more info: anilist character <id>")
            embeds.append(embed)        
         
        if anime.description():
            texts = wrap(anime.description(), 1024, replace_whitespace = False)    
            for text in texts:
                embed = self.bot.get_embed(title = "Description", description = text)
                embeds.append(embed)           
          
        pages = InteractionCheckButtonMenuPages(            
            ctx = ctx, 
            source = ListPageSource(embeds),
            clear_buttons_after = True,
            timeout = self.bot.pagination_timeout
        )
        await pages.start(ctx)     

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(
        name = "tracemoe",      
        aliases = [],
        help = "[attachment] <cut_borders=0> <video=0>"
    )
    async def tracemoe(
        self, 
        ctx, 
        params: commands.Greedy[KeywordArgumentConverter()]
    ):
        args = dict((x, y) for x, y in params)        
        
        if not ctx.message.attachments:
            raise commands.BadArgument()
            
        url = ctx.message.attachments[0].url 
        
        try:
            anime = await self.tracemoe.search(url, int(args.get("cut_borders", 0)), 1)           
        except:
            raise commands.BadArgument()
            
        if anime.raw.get("error"):            
            raise self.bot.error(anime.get("error_desc", "unknown"))             
                                
        time_from = anime.time().get("from")
        time_to = anime.time().get("from")
        time = ""
        
        if any(list(time_from.values())):
            time += "from: "
            if time_from.get("hours"):
                time += str(time_from.get("hours")) + ":"
                
            if time_from.get("minutes"):
                time += str(time_from.get("minutes")) + ":"
                
            if time_from.get("seconds"):
                time += str(time_from.get("seconds")) + ":"
            
        if any(list(time_to.values())):
            time += "\nto: "
            if time_to.get("hours"):
                time += str(time_to.get("hours")) + ":"
                
            if time_to.get("minutes"):
                time += str(time_to.get("minutes")) + ":"
                
            if time_to.get("seconds"):
                time += str(time_to.get("seconds")) + ":"
            
        info = await self.client.get_anime_with_id(anime.id()) if anime.id() else None  
        
        fields = [
            ("Name:", info.title(), False) if info.title() else None,              
            ("Anilist Id:", anime.id(), False) if anime.id() else None,
            ("Episode:", anime.episode(), False) if anime.episode() else None,
	           ("Time:", time, False) if time else None,
            ("Similarity:", anime.similarity(), False) if anime.similarity() else None  
        ]
        
        embed = self.bot.get_embed(fields = fields)
        embed.set_image(url = anime.image()) if anime.image() else None
        
        if not args.get("video"):
            await ctx.channel.send(embed = embed)
        else:
            await ctx.channel.send(anime.video())

def setup(bot):
    bot.add_cog(Anime(bot))        