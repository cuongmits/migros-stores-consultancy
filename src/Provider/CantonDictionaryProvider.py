# TODO: Move this file into Provider folder, not the same folder with HomePage.py

import json

def getCantonDictionary():
    data = json.load(open("./data/raw/gemeinden-json.json"))
    
    return data