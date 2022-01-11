from mymodule.myloader import *
from gensim.models import KeyedVectors

import numpy as np
import pandas as pd
import os
import regex as  re

def main():
    
    all_res = []

    wv = KeyedVectors.load('./patent_w2v_iter5.model') #学習済みモデル(wmDistance)
    print("LOAD SUCCESS")

    #LOAD BanWord FILE
    Ban_words = load_jsonfile("./out2/listbannounwords.json")
    key_ban = Ban_words.keys()

    #LOAD 発明の効果 FILE
    Invention = load_jsonfile("./out2/out-invention-filterd.json")
    key_inv = Invention.keys()

    #FIND DISTANCE#
    out = load_jsonfile("./template.json")
    save_file_path = "./out2/pdfile/"
    for patent_name in Ban_words.keys():  
        remain = []
        print(patent_name)
        if Ban_words[patent_name] == [] or Ban_words[patent_name] == None:
            continue
        else:
            Bans = Ban_words[patent_name]

        if Invention[patent_name] == []  or Invention[patent_name] == None:
            continue
        else:
            Invents = Invention[patent_name]

        distance = pd.DataFrame(0.0, index=Bans, columns=Invents)
        for inv in Invents:
            for ban in Bans:
                x = wv.wmdistance(inv,ban)
                distance[inv][ban] = x
                all_res.append(x)
                if(x >= 2.4):
                    remain.append(inv)

        Invention[patent_name] = list(set(remain))

        save_picklefile(save_file_path+patent_name+".pd", distance)

    save_picklefile("./out2/allvalue.lst", all_res)

    save_jsonfile("./out2/inv-filt-with-distance.json", Invention)

def main2():

    all_res = []
    all_ban_words = []
    all_inv_words = []
    wv = KeyedVectors.load('./patent_w2v_iter5.model') #学習済みモデル(wmDistance)
    print("LOAD SUCCESS")
    #LOAD BanWord FILE
    Ban_words = load_jsonfile("./out2/listbannounwords.json")
    key_ban = Ban_words.keys()
    #LOAD 発明の効果 FILE
    Invention = load_jsonfile("./out2/out-invention-filterd.json")
    key_inv = Invention.keys()

    for i in Ban_words.values():
        if(i != None):
            all_ban_words.extend(i)

    #FIND DISTANCE#
    out = load_jsonfile("./template.json")
    save_file_path = "./out2/pdfile2/"
    throw = set()
    for patent_name in out.keys():  
        
        print(patent_name)
        if Invention[patent_name] == []  or Invention[patent_name] == None:
            continue
        else:
            Invents = Invention[patent_name]

        distance = pd.DataFrame(0.0, index=all_ban_words, columns=Invents)
        print(distance.shape)
        for inv in Invents:
            for ban in all_ban_words:
                x = wv.wmdistance(inv,ban)
                distance[inv][ban] = x
                all_res.append(x)
                if(x <= 2.4):
                    if(inv=="非晶質合金製構造部材"):
                        print(inv)
                    throw.add(inv)

        save_picklefile(save_file_path+patent_name+".pd", distance)

    print(throw)
    save_picklefile("./out2/from_all_ban_words.set", throw)
    save_picklefile("./out2/allvalue2.lst", all_res)
    for patent_name in Invention:
        if(Invention[patent_name] != None):
            Invention[patent_name] = set(Invention[patent_name])
            Invention[patent_name] = list(Invention[patent_name] - throw)



    save_jsonfile("./out2/inv-filt-with-distance2.json", Invention)

if __name__ == "__main__":
    
    #main()
    #main2()
    
    ### FILTERED VERSION
    
    dict_eff_words = load_jsonfile("./out2/inv-filt-with-distance.json")
    res = dict.fromkeys(dict_eff_words.keys())

    for patent_name in dict_eff_words:
        
        if(dict_eff_words[patent_name] == None):
            continue

        unfiltered_list = dict_eff_words[patent_name]
        filtered_res = []
        no_need_word = []

        print(patent_name)

        for word in unfiltered_list:
            pattern = ".*合金$|.*材料$|.*粉末$|.*発明.*|.*粉|.*実施.*|.*例.*|.*時"
            temp = re.findall(pattern, word)
            while '' in temp:
                temp.remove('')
            no_need_word.extend(temp)

        filtered_res = set(unfiltered_list) - set(no_need_word)
        res[patent_name] = list(filtered_res)

    save_jsonfile("./out2/inv_filt_with_dist_after_discarding.json", res)

    
    













