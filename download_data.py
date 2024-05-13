import urllib.request, json
import sys
import os

save_path="./data/xeno-canto/"

# with open('bird_names.txt') as f:
#     bird_names = f.readlines()
# bird_names = [n.strip() for n in bird_names]

bird_names = ["Parus major"]

for name in bird_names:
    url = f'https://www.xeno-canto.org/api/2/recordings?query=cnt:poland%20grp:birds%20type:song%20{name.replace(' ', '%20')}&page=1'
    jsonPage = urllib.request.urlopen(url)
    jsonData = json.loads(jsonPage.read().decode('utf-8'))
    print("downloading", len(jsonData['recordings']), "recordings of", name)
    if not os.path.exists(save_path + name):
        os.makedirs(save_path + name)  
    for i, recording in enumerate(jsonData['recordings']):
        url = recording['file']
        urllib.request.urlretrieve(url, save_path + name + '/' + name + "_" + str(i) + '.mp3')

# jsonPage = urllib.request.urlopen("https://www.xeno-canto.org/api/2/recordings?query=cnt:poland%20grp:birds%20type:song%20Parus%20major&page=1")
# jsonData = json.loads(jsonPage.read().decode('utf-8'))
# url = jsonData['recordings'][4]['file']
# urllib.request.urlretrieve(url, './data/bogatka.mp3')