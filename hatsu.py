import pickle
from typing import Pattern
import spacy
from spacy.matcher import Matcher
import os
import ginza 
import regex as re

from mymodule.myloader import * 
from mymodule.findWords import *

patents_list = load_picklefile("./patent.object")

nlp = spacy.load("ja_ginza")

FindProcessWord = Matcher(nlp.vocab)
pattern  = [{"TEXT":"に"}, {"LEMMA": "よる"}]
pattern2 = [{"TEXT":"で"}, {"TEXT":"は", "POS":"*"}]
pattern3 = [{"OP":"*"}, {"TEXT":"から"}] 
pattern4 = [{"OP":"*"}, {"TEXT":"ので"}] 
FindProcessWord.add("con", None, pattern)
FindProcessWord.add("con", None, pattern2)
FindProcessWord.add("con", None, pattern3)
FindProcessWord.add("con", None, pattern4)

path = './effect_words/'
effect_words = os.listdir(path)
res = dict.fromkeys(effect_words)

#辞書resの初期化
objec = ["compound_word", "Noun_before_TWord", "Not_Noun"]

for name in effect_words:
    res[name] = dict.fromkeys(objec)

print(res[effect_words[0]])

i = 0
for patent in patents_list:

    #if(patent.name != "1992317306.txt"):
    #    continue

    print(patent.name)
    

    for inv_word in patent.doc_invention:

        inv_word_splitByDot = re.split('。', inv_word)

        while "" in inv_word_splitByDot:
            inv_word_splitByDot.remove("")
            
        for inv_word_smallPart in inv_word_splitByDot:

            inv_word_splitByComma = re.split("、", inv_word_smallPart)
            while "" in inv_word_splitByComma:
                inv_word_splitByComma.remove("")

            for sentence in inv_word_splitByComma:    
                 
                doc = nlp(sentence)
                found = FindProcessWord(doc)
                
                if (len(found) >= 1):
                    
                    kekka = find_noun_and_compound(doc, i)
                    if(res[patent.name]["Noun_before_TWord"] == None):
                        res[patent.name]["Noun_before_TWord"] = kekka
                    else:
                        res[patent.name]["Noun_before_TWord"].extend(kekka)
                else:
           
                    kekka = find_noun_and_compound(doc, i)
                    if(res[patent.name]["compound_word"] == None):
                        res[patent.name]["compound_word"] = kekka
                    else:
                        res[patent.name]["compound_word"].extend(kekka)

    #if(res[patent.name]["Noun_before_TWord"] != None and res[patent.name]["compound_word"] != None):
    #    same = set(res[patent.name]["Noun_before_TWord"])&set(res[patent.name]["compound_word"])
    #    res[patent.name]["compound_word"] = list(set(res[patent.name]["compound_word"]) - same)
    
save_jsonfile("./out/out-invention.json", res)



path = './effect_words/'
effect_words = os.listdir(path)
res = dict.fromkeys(effect_words)
patent_list_word = load_jsonfile("./out/out-invention.json")


i = 0
for patent_name in patent_list_word.keys():

    #if(patent_name != "1992000303.txt"):
    #    continue

    unfiltered_list = patent_list_word[patent_name]["compound_word"]
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

save_jsonfile("out-invention-filtered.json", res)
