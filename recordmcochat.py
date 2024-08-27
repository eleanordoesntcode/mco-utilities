import aiohttp
import asyncio
import time
import html

async def requestmorelog():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://minecraftonline.com/cgi-bin/tailminecraftlog.sh') as r:
            returns = await r.text(encoding="utf-8")
            return(returns)

def recordchat(text):
    print(text)
    f = open("log.txt", mode="a+")
    f.write(text)
    f.close()
    return(None)

async def mainloop(lastchunk):
    starttime = time.time()
    newchunk = await requestmorelog()
    newchunk = newchunk.replace("<br />", "")
    newchunk = html.unescape(newchunk)
    if newchunk != lastchunk:
        currdate = time.strftime('%Y-%m-%d %H:%M:%S')
        recordchat(f"[{currdate}] New chunk recieved:\n{newchunk}\n")
        lastchunk = newchunk
    if time.time() - starttime < 2:
        time.sleep(2-(time.time() - starttime))
    return(newchunk)
# we first initiate the log
currdate = time.strftime('%Y-%m-%d %H:%M:%S')
recordchat(f"[{currdate}] Starting logging\n")
lastchunk = ""
while True:
    lastchunk = asyncio.run(mainloop(lastchunk))
