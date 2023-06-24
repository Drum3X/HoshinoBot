#discord modules
from discord.ext import commands

#python modules
from re import match

class KeywordArgumentConverter(commands.Converter):
    async def convert(self, ctx, token):
        res = match("(\\w+)(=)(.+)", token)
            
        if not res:
            raise commands.BadArgument()
          
        return (res.groups()[0], res.groups()[2])

class CodeblockConverter(commands.Converter):
    async def convert(self, ctx, code):
        if code.startswith("```") and code.endswith("```"):
            code = "\n".join(code.split("\n")[1:])[:-3]
            
        return code