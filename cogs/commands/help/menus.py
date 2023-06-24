#nextcord modules
from nextcord.ext import menus

class HelpListPageSource(menus.ListPageSource):
    def __init__(self, data, title, bot):
        super().__init__(data, per_page = 4) 
        self.bot = bot
        self.title = title

    async def format_page(self, menu, entries):  
        embed = self.bot.get_embed(title = self.title, fields = entries)
        embed.set_footer(text = f"Page {menu.current_page + 1}/{self.get_max_pages()}") if self.get_max_pages() != 1 else None       
        return embed  