#nextcord modules
import nextcord            

class Embed():    

    def __init__(self, color):
        self.color = color
        
    def get_embed(
        self,        
        title: str = None, 
        description: str = None,                 
        fields: list = [],
        code = False
    ):        
        embed = nextcord.Embed(
            title = str(title) if title else None, 
            description = f"```{'py' if code else ''}\n {str(description)}```" if description else None,
            color = self.color
        )
                
        if fields:
            for field in fields:
                if not field:
                    continue
                  
                embed.add_field(
                    name = str(field[0]), 
                    value = f"```{'py' if code else ''}\n {str(field[1])}```", 
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
      
        await ctx.channel.send(embed = embed)
        