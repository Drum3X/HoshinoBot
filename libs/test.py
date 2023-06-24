from animelib.tracemoe import AsyncTracemoe
from animelib.anilist import AsyncClient
import asyncio

cli = AsyncClient()
trc = AsyncTracemoe()

async def main():
    return await asyncio.gather(cli.get_anime("re:zero"), trc.search("https://cdn.discordapp.com/attachments/926767811861311508/1107031221667631255/DGo0HjbU0AAbidc-1.jpg"))

print(asyncio.run(main())[0])  