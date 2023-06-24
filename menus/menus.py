#nextcord modules
import nextcord
from nextcord.ext import commands, menus

class InteractionCheckButtonMenuPages(menus.ButtonMenuPages):

    def __init__(self, ctx: commands.Context, **kwargs):
        super().__init__(**kwargs)
        self.ctx = ctx

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        return self.ctx.author == interaction.user

class ListPageSource(menus.ListPageSource):
    def __init__(self, data):        
        super().__init__(data, per_page = 1)

    async def format_page(self, menu, entries): 
        embed = entries.copy()                            
        embed.set_footer(text = f"{embed.footer.text if embed.footer else ''}\nPage {menu.current_page + 1}/{self.get_max_pages()}") if self.get_max_pages() != 1 else None
        
        return embed