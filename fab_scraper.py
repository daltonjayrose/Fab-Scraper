import json
import os
import json
import requests
import time
from types import NoneType
import sys
import urllib.request
import datetime

# FAB Profile Config
# 2 = Heejin, 3 = Hyunjin, 4 = HaSeul, 5 = YeoJin, 6 = ViVi, 
7 = Kim Lip, 8 = JinSoul, 9 = Choerry, 
10 = Yves, 11 = Chuu, 12 = Go Won, 13 = Olivia Hye

fab_profile_id = "13"
fab_profile_url = "https://vip-fab-api.myfab.tv/fapi/2/artists/" + fab_profile_id + "/messages"

if fab_profile_id == "2":
    fab_path = "/docs/Heejin/"
if fab_profile_id == "3":
    fab_path = "/docs/Hyunjin/"
if fab_profile_id == "4":
    fab_path = "/docs/HaSeul/"
if fab_profile_id == "5":
    fab_path = "/docs/YeoJin/"
if fab_profile_id == "6":
    fab_path = "/docs/Vivi/"
if fab_profile_id == "7":
    fab_path = "/docs/Kim Lip/"
if fab_profile_id == "8":
    fab_path = "/docs/JinSoul/"
if fab_profile_id == "9":
    fab_path = "/docs/Choerry/"
if fab_profile_id == "10":
    fab_path = "/docs/Yves/"
if fab_profile_id == "11":
    fab_path = "/docs/Chuu/"
if fab_profile_id == "12":
    fab_path = "/docs/Go Won/"
if fab_profile_id == "13":
    fab_path = "/docs/Olivia Hye/"

# Headers Config
headers = {
	"Host": "vip-fab-api.myfab.tv",
	"User-Agent": "fab|android|playstore|1.3.2|11|sdk_gphone_x86_64_arm64|google|en|US",
	"userid": "REDACTED",
	"accesstoken": "REDACTED"
}

# Retrieve Json from Fab
fab_profile = requests.get(fab_profile_url, headers=headers).json()
dir_path = os.getcwd()
fab_profile_json = json.dumps(fab_profile)

# Iterate through posts, retrieving post ids.
for posti in range(len(fab_profile['messages'])):
    fab_post_id_int = fab_profile['messages'][posti]['id']
    fab_post_id = str(fab_post_id_int)
    fab_post_url = "https://vip-fab-api.myfab.tv/fapi/2/users/REDACTED/message/" + fab_post_id + "/ncomments"

# Get timestamp of Fab post and convert it to date/time
    fab_post_timestamp = fab_profile['messages'][posti]['publishedAt']
    fab_post_date = datetime.date.fromtimestamp(fab_post_timestamp/1000)

# Retrieve post Json from Fab
    fab_post = requests.get(fab_post_url, headers=headers).json()

# Write post Json to file
    fab_post_json = json.dumps(fab_post)
    with open(dir_path + fab_path + '%s %snew.json' % (fab_post_date, fab_post_id), 'w+', encoding='UTF-8') as outfile:
        outfile.write(fab_post_json)
    fab_json_current_exists = os.path.exists(dir_path + fab_path + '%s %s.json' % (fab_post_date, fab_post_id))
    if fab_json_current_exists == False:
        with open(dir_path + fab_path + '%s %s.json' % (fab_post_date, fab_post_id), 'w+', encoding="UTF-8") as outfile:
            outfile.write("Empty json")  

# Compare new Json to current Json to check for updates
    fab_json_size_new = os.stat(dir_path + fab_path + '%s %snew.json' % (fab_post_date, fab_post_id))
    fab_json_size_current = os.stat(dir_path + fab_path + '%s %s.json' % (fab_post_date, fab_post_id))
    print(fab_post_id)
# If Json has been updated, remove the current Json and rename new Json to current
    if fab_json_size_new > fab_json_size_current or fab_json_current_exists == False:
        os.remove(dir_path + fab_path + '%s %s.json' % (fab_post_date, fab_post_id))
        os.rename(dir_path + fab_path + '%s %snew.json' % (fab_post_date, fab_post_id), dir_path + fab_path + '%s %s.json' % (fab_post_date, fab_post_id))
        fab_md_exists = os.path.exists(dir_path + fab_path + '%s %s.md' % (fab_post_date, fab_post_id))

# Skip file if md exists.
        if fab_md_exists == True:
            #os.remove(dir_path + fab_path + '%s %s.md' % (fab_post_date, fab_post_id))
            continue

# Retrieve comments through iteration
        for commenti in range(len(fab_post['comments'])):
            fab_comment = fab_post['comments'][commenti]['comment']
            fab_quote = fab_post['comments'][commenti]['quotedComment']

# Discard result if comment is of type NoneType
            if isinstance(fab_comment, NoneType):
                    continue
            if isinstance(fab_quote, NoneType) == False:
# Translate quoted comment using Papago
            # Naver Papago Config
                try:
                    client_id = "REDACTED"
                    client_secret = "REDACTED"
                    data = "source=ko&target=en&text=" + fab_quote
                    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
                    request = urllib.request.Request(url)
                    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
                    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
                    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                    rescode = response.getcode()
                    if(rescode==200):
                        response_body = response.read()
                        print(response_body.decode('utf-8'))
                    else:
                        print("Error Code:" + rescode)
                        continue
                    res_body = json.loads(response_body)
                    msg = res_body.get("message")
                    result = msg.get("result", None)
                    translated_text = result.get("translatedText")
                except urllib.error.HTTPError:
                    print("HTTP Error")
# Output comments to md file
                with open(dir_path + fab_path + '%s %s.md' % (fab_post_date, fab_post_id), 'a+', encoding='utf-8') as f:
                    f.write('*"')
                    f.write(translated_text)
                    f.write('"*')
                    f.write("  \n")
                    f.write("  \n")

# Translate comment using Papago
            # Naver Papago Config
            try:
                client_id = "REDACTED"
                client_secret = "REDACTED"
                data = "source=ko&target=en&text=" + fab_comment
                url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
                request = urllib.request.Request(url)
                request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
                request.add_header("X-NCP-APIGW-API-KEY",client_secret)
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if(rescode==200):
                    response_body = response.read()
                    print(response_body.decode('utf-8'))
                else:
                    print("Error Code:" + rescode)
                    continue
                res_body = json.loads(response_body)
                msg = res_body.get("message")
                result = msg.get("result", None)
                translated_text = result.get("translatedText")
            except urllib.error.HTTPError:
                print("HTTP Error")
# Output comments to md file
            with open(dir_path + fab_path + '%s %s.md' % (fab_post_date, fab_post_id), 'a+', encoding='utf-8') as f:
                f.write(translated_text)
                f.write("  \n")
                f.write("  \n")
