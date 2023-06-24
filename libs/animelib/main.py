from anilist import SyncClient

cli = SyncClient()

anime = cli.get_manga("kaguya-sama")


for x in dir(anime):
    if not x.startswith("__"):      
        if x in ["page", "media", "data", "raw", "character"]:
            continue
        
        print(f"\n\n\n{x}\n\n\n")    
        a = getattr(anime, x)()
        print(a)     
