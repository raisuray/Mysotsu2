from mymodule.myloader import *
from gensim.models import KeyedVectors
import pandas as pd 
import sys as sys

shikiichi = 1.9

def is_same(word1, word2):
    distance  = wv.wmdistance(word1, word2)    
    if(distance <= 1.9):
        return 1
    else:
        return 0

my_inv    = load_jsonfile("all_koukago_from_hatsumei.json")
kaede_inv = load_jsonfile("kaede_result.json")

wv = KeyedVectors.load('./patent_w2v_iter5.model')
print("LOAD SUCCESS")

out = load_jsonfile("template.json")
out_kaede = load_jsonfile("template.json")
i = 0



df = pd.DataFrame(0, columns=['my_true', 'total_my'], index=out.keys())


for patent_name in out:

    print(patent_name)
    my_list_word = my_inv[patent_name]
    kaede_list_word = kaede_inv[patent_name][0]["発明の効果"]
    
    if(my_list_word == [] or kaede_list_word == []):
        continue


    out[patent_name] = {'True':set(), 'False':set()}
    out_kaede[patent_name] = {'True':set(), 'False':set()}
    #out[patent_name]['True']  = []
    #out[patent_name]['False'] = []

    #print(my_list_word)
    #print(kaede_list_word)
    try:
        total_word_mine = len(my_list_word)
        total_word_his  = len(kaede_list_word) 
    except:
        continue

    for my_word in my_list_word:
        flag = 0

        for kaede_word in kaede_list_word:
            
            flag = is_same(my_word, kaede_word)
            if (flag == 1):
                out[patent_name]['True'].add(my_word)
                out_kaede[patent_name]['True'].add(kaede_word)
            else:
                out_kaede[patent_name]['False'].add(kaede_word)
            
        if(flag ==  0):
            if(my_word not in out[patent_name]['True']):
                out[patent_name]['False'].add(my_word)
    
    
    print("TOTAL TRUE = {0} / {1}, My TOTAL WORD = {0} / {2}".format(len(out[patent_name]['True']), total_word_his, total_word_mine))
    print("From kaede result ## True : {}, False : {}".format(out_kaede[patent_name]['True'], out_kaede[patent_name]['False']))
    df['my_true'][patent_name] += len(out[patent_name]['True'])
    df['total_my'][patent_name] += total_word_mine
    i+=1
    print(out[patent_name])

#print('Total True : {} / {} ==== {}%'.format(my_true, total_my, my_true/total_my))
print(df['my_true'].sum()/df['total_my'].sum())
print(df)

