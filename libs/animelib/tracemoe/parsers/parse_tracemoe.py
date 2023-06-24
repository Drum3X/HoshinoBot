#python modules
from datetime import timedelta

class ParseTracemoe():
    def __init__(self, data, page: int = 1): 
        self.raw = data   
                        
        try:
            self.data = data.get("result")[page - 1]
        except:
            self.data = data                
        
    def __dict__(self):                 
        return self.raw

    def id(self):
        return self.data.get("anilist")      
        
    def filename(self):                       
        return self.data.get("filename")
    
    def video(self):                       
        return self.data.get("video")
        	   
    def image(self):                       
        return self.data.get("image")
        	   
    def episode(self):
        return self.data.get("episode")
                
    def time(self):
        if not self.data.get("from") or not self.data.get("to"):
            return 
            
        from_time = timedelta(seconds = self.data.get("from"))
        to_time = timedelta(seconds = self.data.get("to"))
           
        time = {
            "from": {
				            "raw": self.data.get("from"),                                
				            "hours": int(from_time.seconds / 3600),
				            "minutes": int(from_time.seconds % 3600 / 60),
				            "seconds": int(from_time.seconds % 3600 % 60),
				            "miliseconds": int(from_time.microseconds)
            },
            "to": {
               "raw": self.data.get("to"),                                
				            "hours": int(to_time.seconds / 3600),
				            "minutes": int(to_time.seconds % 3600 / 60),
				            "seconds": int(to_time.seconds % 3600 % 60),
				            "miliseconds": int(to_time.microseconds)              
            }   
        }  
            
        return time
        
    def similarity(self):
        if self.data.get("similarity"):
            return round((self.data.get("similarity") * 100), 2)          
    