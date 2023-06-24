#python modules
from re import compile, sub
from time import localtime
from datetime import timedelta

class ParseAnime():
    def __init__(self, data):
        self.raw = data         
        self.page = self.raw.get("Page")    
        self.media = self.page.get("media")            
        
        if self.media:
            self.data = self.media[0]
        else:
            self.data = {}        	           
  
    def page_info(self):       
        return self.page.get("pageInfo")         
        	            
    def id(self):                
        return self.data.get("id")                   
        
    def title(self, lang: str = "romaji"):                                 
        title = self.data.get("title")
        
        return title.get(lang, title.get("romaji"))
                        
    def url(self):        
        return self.data.get("siteUrl")                   
                    
    def episodes(self):       
        return self.data.get("episodes")                  
                    
    def description(self):       
        desc = self.data.get("description")
            
        if not desc:
            return 
                
        tag = compile("<.*?>")
        
        return sub(tag, "", desc)
        
    def format(self):        
        return self.data.get("format")

    def status(self):       
        return self.data.get("status")
        
    def duration(self):      
        return self.data.get("duration")
                                       
    def genres(self):       
        return self.data.get("genres")                    
                    
    def is_adult(self):        
        return self.data.get("isAdult")
                                        
    def tags(self):        
        tags = self.data.get("tags")
            
        if not tags:
            return 
                
        list = [tag.get("name") for tag in tags]
                                               
        return list                    
                    
    def studios(self):        
        studios = self.data.get("studios")
            
        if studios:
            return studios.get("nodes")       
                                
    def start_date(self):                
        return self.data.get("startDate")
                                
    def end_date(self):        
        return self.data.get("endDate")
     
    def season(self):        
        return self.data.get("season")
       
    def origin(self):       
        return self.data.get("countryOfOrigin")                    
                    
    def image(self, size: str = "large"):                                    
        image = self.data.get("coverImage")
        
        return image.get(size, image.get("large"))
         
    def banner(self):        
        return self.data.get("bannerImage")                    
                    
    def source(self):        
        return self.data.get("source")

    def hashtag(self):       
        return self.data.get("hashtag")                  
                    
    def synonyms(self):        
        return self.data.get("synonyms")                   
                    
    def score(self, type: str = "mean"):        
        keys = {
            "mean": "meanScore", 
            "average": "averageScore"
        }

        return self.data.get(keys.get(type, "meanScore"))                       
                       
    def popularity(self):       
        return self.data.get("popularity")                   
                    
    def rankings(self):        
        return self.data.get("rankings")
                    
    def next_episode(self):        
        next_episode = self.data.get("nextAiringEpisode")
            
        if not next_episode:
            return 
                
        air_time = localtime(next_episode.get("airingAt", 0))
        time_until_air = timedelta(seconds = next_episode.get("timeUntilAiring", 0))        
                        
        dict = {
            "air_time": {
                "raw": next_episode.get("airingAt"),
                "year": air_time.tm_year,
                "month": air_time.tm_mon,
                "day": air_time.tm_mday,
                "hour": air_time.tm_hour,
                "minute": air_time.tm_min,
                "struct": air_time
            },       
                                     
            "time_until_air": {
                "raw": next_episode.get("timeUntilAiring"),                
                "days": int(time_until_air.days),
                "hours": int(time_until_air.seconds / 3600),
                "minutes": int(time_until_air.seconds % 3600 / 60),
                "seconds": int(time_until_air.seconds % 3600 % 60)
            },               
                    
            "episode": next_episode.get("episode")
        }
            
        return dict                    
                        
    def trailer(self):        
        trailer = self.data.get("trailer")
            
        if not trailer:
            return 
            
        dict = {
            "link": None,
            "site": trailer.get("site"),
            "thumbnail": trailer.get("thumbnail")
        }
            
        if trailer.get("site") == "youtube":
            dict["link"] = "https://youtu.be/" + trailer.get("id")
                
        return dict
                                       
    def staff(self):        
        staffs = self.data.get("staff").get("edges")
            
        if not staffs:
            return 
                
        list = []
        for staff in staffs:
            node = staff.get("node")
            name = node.get("name")
            dict = {
                "id": node.get("id"),
                "first": name.get("first"),
                "last": name.get("last"),
                "full": name.get("full"),
                "native": name.get("native"),
                "role": staff.get("role")
            }
            list.append(dict)
                
        return list
        
            
                    
    def characters(self):       
        characters = self.data.get("characters").get("edges")
            
        if not characters:
            return 
                
        list = []
        for character in characters:
            node = character.get("node")
            name = node.get("name")
            dict = {
                "id": node.get("id"),
                "first": name.get("first"),
                "last": name.get("last"),
                "full": name.get("full"),
                "native": name.get("native"),
                "role": character.get("role"),
                "favourites": node.get("favourites")
            }
            list.append(dict)
                
        return list                            
                    
    def relations(self):       
        relations = self.data.get("relations").get("edges")
            
        if not relations:
            return 
                
        list = []
        for relation in relations:   
            node = relation.get("node")                   
            dict = {
                "id": node.get("id"),
                "relation": relation.get("relationType"),
                "title": node.get("title"),                                
                "type": node.get("type")
            }
            list.append(dict)
                
        return list
        
                        