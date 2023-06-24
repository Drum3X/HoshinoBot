async def get_blacklist(bot):
    async with bot.db.execute("select ids from blacklist") as cursor:            
        blacklist = [user[0] for user in await cursor.fetchall()]              
        
    return blacklist