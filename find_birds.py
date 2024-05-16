import urllib.request, json
import pandas as pd
import sys
import os

with open('bird_names.txt') as f:
    bird_names = f.readlines()
bird_names = [n.strip() for n in bird_names]

num_recordings = []
for i, name in enumerate(bird_names):
    url = f"https://www.xeno-canto.org/api/2/recordings?query=cnt:poland%20grp:birds%20type:song%20{name.replace(' ', '%20')}&page=1"
    jsonPage = urllib.request.urlopen(url)
    jsonData = json.loads(jsonPage.read().decode('utf-8'))
    num_recordings.append(len(jsonData['recordings']))
    print("bird", str(i) + "/" + str(len(bird_names)))

df = pd.DataFrame({
    "name": bird_names,
    "num_recordings": num_recordings
})

df = df.sort_values(by="num_recordings", ascending=False)
print(df.head(10))

# top 10: 
# Parus major             266 (bogatka)
# Emberiza citrinella     250 (trznadel)
# Sylvia atricapilla      232 (kapturka)
# Fringilla coelebs       230 (zięba)
# Phylloscopus collybita  224 (pierwiosnek)
# Turdus philomelos       212 (śpiewak)
# Periparus ater          176 (sosnówka)
# Erithacus rubecula      176 (rudzik)
# Turdus merula           163 (kos)
# Aegolius funereus       158 (włochatka)