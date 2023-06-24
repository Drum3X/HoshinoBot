#nextcord modules
import nextcord            

class Embed():    
    def __init__(self, color):
        self.color = color
        
    def get_embed(
        self,        
        title: str = None, 
        description: str = None,                 
        fields: list = []
    ):        
        embed = nextcord.Embed(
            title = str(title) if title else None, 
            description = "```py\n" + str(description) + "```" if description else None,
            color = self.color
        )
                
        if fields:
            for field in fields:               
                embed.add_field(
                    name = str(field[0]), 
                    value = "```py\n" + str(field[1]) + "```" if field[1] else None, 
                    inline = field[2]
                )
                        
        return embed                   
        
    async def send_embed(
        self,
        ctx, 
        title: str = None, 
        description: str = None,                 
        fields: list = []
    ):        
        embed = self.get_embed(title = title, description = description, fields = fields)
      
        return await ctx.channel.send(embed = embed)
        