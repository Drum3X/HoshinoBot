#python modules
from aiohttp import ClientSession

#import queries
from .queries import AnilistQuery

#import parsers
from .parsers import (
    ParseAnime, 
    ParseManga, 
    ParseCharacter
)

class AsyncClient(AnilistQuery):
    def __init__(self):
        super().__init__()        
            
    async def _get_data(
        self,         
        query: str, 
        variables: dict,
    ):                
              								
        async with ClientSession() as cs:
            async with cs.post(self._url, json = {"query": query, "variables": variables}) as result:
                data = await result.json()
                
        return data
        
    async def get_anime_with_id(
        self, 
        id: int, 
    ):
        
        data = await self._get_data(self._anime_with_id, self._get_id_variables(id))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("media"):
            return
          
        return ParseAnime(result)
        
    async def get_manga_with_id(
        self, 
        id: str, 
    ):
        
        data = await self._get_data(self._manga_with_id, self._get_id_variables(id))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("media"):
            return
       
        return ParseManga(result)
        
    async def get_character_with_id(
        self, 
        id: int, 
    ):
        
        data = await self._get_data(self._character_with_id, self._get_id_variables(id))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("characters"):
            return
   
        return ParseCharacter(result)
      
    async def get_anime(
        self, 
        search: str, 
        page: int = 1
    ):
        
        data = await self._get_data(self._anime, self._get_search_variables(search, page))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("media"):
            return
  
        return ParseAnime(result)
       
    async def get_manga(
        self, 
        search: str, 
        page: int = 1
    ):
        
        data = await self._get_data(self._manga, self._get_search_variables(search, page))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("media"):
            return

        return ParseManga(result)
        
    async def get_character(
        self, 
        search: str, 
        page: int = 1
    ):
        
        data = await self._get_data(self._character, self._get_search_variables(search, page))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("characters"):
            return
 
        return ParseCharacter(result)        
