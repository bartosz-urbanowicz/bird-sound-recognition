import urllib.request, json
import os

save_path="./data/xeno-canto/"

bird_names = [
    "Parus major",
    "Emberiza citrinella",
    "Sylvia atricapilla",
    "Fringilla coelebs",
    "Phylloscopus collybita",
    "Turdus philomelos",
    "Periparus ater",
    "Erithacus rubecula",
    "Turdus merula",
    "Aegolius funereus"
    ]

for name in bird_names:
    url = f"https://www.xeno-canto.org/api/2/recordings?query=cnt:poland%20grp:birds%20type:song%20{name.replace(' ', '%20')}&page=1"
    jsonPage = urllib.request.urlopen(url)
    jsonData = json.loads(jsonPage.read().decode('utf-8'))
    print("downloading", len(jsonData['recordings']), "recordings of", name)
    if not os.path.exists(save_path + name):
        os.makedirs(save_path + name)  
    for i, recording in enumerate(jsonData['recordings']):
        url = recording['file']
        urllib.request.urlretrieve(url, save_path + name + '/' + name + "_" + str(i) + '.mp3')