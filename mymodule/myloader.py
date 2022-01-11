import json
import pickle

def load_jsonfile(path):
    with open(path, "r") as f:
        x = json.load(f)
    return x

def save_jsonfile(path, value):
    with open(path, 'w') as f:
        json.dump(value, f, indent=4, ensure_ascii=False)

def load_picklefile(path):
    with open(path, "rb") as f:
        x = pickle.load(f)
    return x

def save_picklefile(path, value):
    with open(path, "wb") as f:
        x = pickle.dump(value, f)
