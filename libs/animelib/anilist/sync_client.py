#python modules
from requests import post

#import queries
from .queries import AnilistQuery

#import parsers
from .parsers import (
    ParseAnime, 
    ParseManga, 
    ParseCharacter
)

class SyncClient(AnilistQuery):
    def __init__(self):
        super().__init__()
            
    def _get_data(
        self,         
        query: str, 
        variables: dict,
    ):                
              								        
        data = post(self._url, json = {"query": query, "variables": variables}).json()       
                              
        return data
        
    def get_anime_with_id(
        self, 
        id: int, 
    ):
        
        data = self._get_data(self._anime_with_id, self._get_id_variables(id))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("media"):
            return
       
        return ParseAnime(result)
        
    def get_manga_with_id(
        self, 
        id: str, 
    ):
        
        data = self._get_data(self._manga_with_id, self._get_id_variables(id))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("media"):
            return
        
        return ParseManga(result)
        
    def get_character_with_id(
        self, 
        id: int, 
    ):
        
        data = self._get_data(self._character_with_id, self._get_id_variables(id))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("characters"):
            return
                 
        return ParseCharacter(result)
      
    def get_anime(
        self, 
        search: str, 
        page: int = 1
    ):
        
        data = self._get_data(self._anime, self._get_search_variables(search, page))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("media"):
            return
          
        return ParseAnime(result)
       
    def get_manga(
        self, 
        search: str, 
        page: int = 1
    ):
        
        data = self._get_data(self._manga, self._get_search_variables(search, page))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("media"):
            return
                              
        return ParseManga(result)
        
    def get_character(
        self, 
        search: str, 
        page: int = 1
    ):
        
        data = self._get_data(self._character, self._get_search_variables(search, page))
        
        if "errors" in data.keys():
            return 
            
        result = data.get("data")
        page = result.get("Page")
        
        if not page.get("characters"):
            return
  
        return ParseCharacter(result)