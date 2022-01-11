from mymodule.myloader import  * 
import regex as re
import sys
import spacy
import numpy as np

nlp = spacy.load('ja_ginza')

koukago_inv = load_jsonfile("all_koukago_from_hatsumei.json")
koukago_exp = load_jsonfile("all_koukago_from_jisshirei.json")
patent_list =  load_picklefile("patent_new.object")
distance = load_jsonfile("distance_T.json")

patent_name =  list(koukago_exp.keys())

name = input("特許文書のファイル名前を入力してください = ")

if name not in patent_name:
    print("ファイルはありません")
    sys.exit()

koukago_inv = koukago_inv[name]
koukago_exp = koukago_exp[name]

for p in range(len(patent_list)):
    if patent_list[p].name == name:
        patent = patent_list[p]


print(patent.name)
print("実施例にある効果語らしい = ", koukago_exp)
print("発明の効果の効果語       = ", koukago_inv)   
print('＝'*32)

info = distance[patent.name]
for exp, inv, dist in info:
    print("Distance : {}".format(dist))
    #show on koukagobun
    for sent in patent.new_doc_inv_word:
        if (len(re.findall(inv,sent)) != 0):
            print("発明の効果： [" + inv + " ]")
            print("・＞", end='')
            print(sent)
    print("-"*32)
    #show on jisshirei
    for sent in patent.doc_experiment:
        if (len(re.findall(exp,sent)) != 0):
            print("実施例 : [ " + exp + " ]")
            print("・＞", end='')
            print(sent)
    
    print('＝'*32)