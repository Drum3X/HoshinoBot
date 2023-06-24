#python modules
from re import compile, sub

class ParseCharacter():
    def __init__(self, data):
        self.raw = data    
        self.page = self.raw.get("Page")         
        self.media = self.page.get("characters")

        if self.media:
            self.data = self.media[0]
        else:        	   
        	   self.data = {}               	          
 
    def page_info(self):        
        return self.page.get("pageInfo")                 	    
            
    def id(self):        
        return self.data.get("id")                            
        
    def name(self, type: str = "full"):                               
        name = self.data.get("name")
        
        return name.get(type, name.get("full"))
           
    def image(self, size: str = "large"):                                           
        image = self.data.get("image")
        
        return image.get(size, image.get("large"))            
             
    def url(self):       
        return self.data.get("siteUrl")                  
        
    def favourites(self):        
        return self.data.get("favourites")                  
        
    def description(self):        
        desc = self.data.get("description")
            
        if not desc:
            return 
                
        tag = compile("<.*?>")
        
        return sub(tag, "", desc)
                              
    def relations(self):        
        relations = self.data.get("media").get("edges")
            
        if not relations:
            return 
                
        list = []
        for relation in relations:   
            node = relation.get("node")                  
            relation = {
                "id": node.get("id"),                
                "title": node.get("title"),                                
                "type": node.get("type")
            }
            list.append(relation)
                
        return list          
                   