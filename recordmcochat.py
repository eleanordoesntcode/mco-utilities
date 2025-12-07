import requests
import time
import html

delay = 2
filename = "log.txt"

def requestmorelog():
    try:
        r = requests.get('https://minecraftonline.com/cgi-bin/tailminecraftlog.sh')
        r2 = requests.utils.get_unicode_from_response(r)
    except Exception as e:
        print("An error occured when fetching the log -", repr(e))
    return(r2)

def recordchat(text):
    print(text)
    f = open(filename, mode="a+")
    f.write(text+"\n")
    f.close()
    return(None)

def mainloop(lastchunk):
    starttime = time.time()
    newchunk = requestmorelog()
    newchunk = newchunk.replace("<br />", "")
    newchunk = html.unescape(newchunk)
    if newchunk != lastchunk:
        print("")
        currdate = time.strftime('%Y-%m-%d %H:%M:%S')
        recordchat(f"[{currdate}] New chunk recieved:\n{newchunk}")
        lastchunk = newchunk
    else:
        print(".", end=" ", flush=True)
    if time.time() - starttime < delay:
        time.sleep(2-(time.time() - starttime))
    return(newchunk)
# we first initiate the log
currdate = time.strftime('%Y-%m-%d %H:%M:%S')
recordchat(f"[{currdate}] Starting logging")
lastchunk = ""
while True:
    lastchunk = mainloop(lastchunk)
