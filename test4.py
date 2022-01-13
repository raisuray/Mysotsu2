from mymodule.myloader import *

hatsumei_wiki = load_jsonfile('all_koukago_from_hatsumei_wikipedia.json')
hatsumei   = load_jsonfile('all_koukago_from_hatsumei.json')

out = load_jsonfile('template.json')

kekka = set()

for patent_name in out:

    if(hatsumei_wiki[patent_name] == None):
        hatsumei_wiki[patent_name] = set()
        wiki = set(hatsumei_wiki[patent_name])
    else:
        wiki = set(hatsumei_wiki[patent_name])

    if(hatsumei[patent_name] == None):
        hatsumei[patent_name] = set()
        hatsu = set(hatsumei[patent_name])
    else:
        hatsu = set(hatsumei[patent_name])


    out[patent_name] = list(wiki-hatsu)

save_jsonfile('missing_in_2files.json', out)

