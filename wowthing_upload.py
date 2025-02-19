# Description: This script is used to find the path(s) of WoWthing_Collector.lua 
# files under the World of Warcraft directory and upload them to the WoWthing API.
#
# Relevant crontab: 
# 5 * * * * /path/to/python3 /path/to/script/wowthing_upload.py > /dev/null 2>&1

import subprocess
import requests
from pathlib import Path
import os
import time
import datetime

wowpath = "/Applications/World of Warcraft" #Path to your world of warcraft
url = "https://wowthing.org/api/upload/"
auth = "YOURAPIKEYHERE"
logfile = "YOURLOGFILEHERE" # (e.g. /Users/ola/wowupload.log)

logFile = open(logfile, "a")
logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Starting WoWthing upload\n")

headers = {
    "User-Agent": "WoWthing Sync - python",
    "Content-Type": "application/json"
    }

out = subprocess.check_output(["/usr/bin/find", wowpath, "-name", "WoWthing_Collector.lua"])
out = out.decode("utf-8").strip()

for lFile in out.split('\n'):
    if (int(time.time()) - int(os.stat(lFile).st_mtime) < 300):
        file_content = Path(lFile).read_text()
        data = {
            "apiKey": auth,
            "luaFile": file_content,
            }
        x = requests.post(url, headers=headers, json=data)
        #print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + lFile + " - " + x.text) # DEBUG
        logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + lFile + " - " + x.text + "\n")

logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Finished WoWthing upload\n")
logFile.close()
