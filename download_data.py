import urllib.request, json
import sys
import os

save_path="../data/xeno-canto/"

with open('bird_names.txt') as f:
    bird_names = f.readlines()
bird_names = [n.strip() for n in bird_names]

min_recordings = 50
counter = 0
for name in bird_names:
    url = f'https://www.xeno-canto.org/api/2/recordings?query=cnt:poland%20grp:birds%20type:song%20{name.replace(' ', '%20')}&page=1'
    jsonPage = urllib.request.urlopen(url)
    jsondata = json.loads(jsonPage.read().decode('utf-8'))
    if len(jsondata['recordings']) > min_recordings:
        counter += 1
        print(f"{name} recordings on 1st page:", len(jsondata['recordings']))
    else:
        print(f"{name} has not enough recordings")
print(f"found {counter}/501 species above {min_recordings} recordings")