from mymodule.myloader import * 
from mymodule.findWords import *
from mymodule.discardP import *
import spacy
import pickle
import os

patents_list = load_picklefile("./patent.object")

path = './effect_words/'
effect_words = os.listdir(path)
dict_eff_words = dict.fromkeys(effect_words)


#FIND ALL THE COMPOUND WORD IN ALL FILE#
nlp = spacy.load("ja_ginza")
for patent in patents_list:
    res = []
    list_of_compound_word = []
    print(patent.name)
    #print(len(patent.doc))

    for i in range(len(patent.doc_experiment)):
        
        doc_samp = nlp(patent.doc_experiment[i])
        if(check_symbol(doc_samp) == True and len(patent.doc_experiment[i]) <= 10):
            continue
        list_of_compound_word = find_noun_and_compound(doc_samp, i)
        res.extend(list_of_compound_word)        
    res = list(set(res))
    res = discard_Ascii(res)
    res = discard_word(res)
    dict_eff_words[patent.name] = res

#MAKE AN OUTPUT FILE#
path = "./out/"
with open(path + "out-experiment.json", 'w') as f:
        json.dump(dict_eff_words,f, indent=4, ensure_ascii=False)



### FILTERED VERSION
res = dict.fromkeys(effect_words)
dict_eff_words = load_jsonfile("./out/out-experiment.json")
for patent_name in effect_words:

    #if(patent_name != "1992000303.txt"):
    #    continue

    unfiltered_list = dict_eff_words[patent_name]
    filtered_res = []
    no_need_word = []

    print(patent_name)

    if(unfiltered_list == None): 
        continue

    temp = set(unfiltered_list)

    for word in unfiltered_list:
        pattern = ".*合金$|.*材料$|.*粉末$|.*発明.*|.*粉|.*実施.*|.*例.*"
        temp = re.findall(pattern, word)
        while '' in temp:
            temp.remove('')
        no_need_word.extend(temp)
        
    filtered_res = set(unfiltered_list) - set(no_need_word)
    res[patent_name] = list(filtered_res)
    
save_jsonfile("./out/out-experiment-filtered.json", res)
