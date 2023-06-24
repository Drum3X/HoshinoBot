#python modules
from aiohttp import ClientSession
from requests import get
from urllib.parse import quote_plus

#import parsers
from .parsers import ParseTracemoe

class BaseTracemoe():
	   
	   _apiurl = "https://api.trace.moe/"
	   _sub = "search?url={}"
	   _cut_sub = "search?cutBorders&url={}"        
	   
	   def _get_url(
	       self, url: str, 
	       cut_borders: bool = False
	   ):
	       
	       if cut_borders:
	       	   return (self._apiurl + self._cut_sub).format(quote_plus(url))
	       else:
	       	   return (self._apiurl + self._sub).format(quote_plus(url))
	       	   
class AsyncTracemoe(BaseTracemoe):    
    def __init__(self):
        super().__init__()        

    async def search(
        self, 
        url: str, 
        cut_borders: bool = False, 
        page: int = 1
    ):        
            
        async with ClientSession() as cs:
            async with cs.get(self._get_url(url, cut_borders)) as result:
                data = await result.json()
    
        if data.get("error"):
            ParseTracemoe({"error": data.get("error")})

        return ParseTracemoe(data, page)           
        
class SyncTracemoe(BaseTracemoe):    
    def __init__(self):
        super().__init__()      

    def search(
        self,
        url: str, 
        cut_borders: bool = False, 
        page: int = 1
    ):        

        data = get(self._get_url(url, cut_borders)).json()
        
        if data.get("error"):
            ParseTracemoe({"error": data.get("error")})

        return ParseTracemoe(data, page)