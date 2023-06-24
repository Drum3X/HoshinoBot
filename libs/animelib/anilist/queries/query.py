#python modules
from importlib.resources import read_text

#import queries
from . import srch, get

class AnilistQuery():  
    _url = "https://graphql.anilist.co"
        
    _anime = read_text(srch, "anime.graphql")
    _manga = read_text(srch, "manga.graphql")
    _character = read_text(srch, "character.graphql")
    _anime_with_id = read_text(get, "anime.graphql")
    _manga_with_id = read_text(get, "manga.graphql")
    _character_with_id = read_text(get, "character.graphql")
    
    def _get_search_variables(
        self, 
        search: str, 
        page: int
    ):
        variables = {
            "search": search,
            "page": page,
            "perPage": 1
        }
        
        return variables
    
    def _get_id_variables(
        self, 
        id: int, 
    ):
        variables = {
            "id": id,
            "page": 1,
            "perPage": 1
        }
        
        return variables
