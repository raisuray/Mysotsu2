import json 
from gensim.models import KeyedVectors
from mymodule.myloader import *

wv = KeyedVectors.load('./patent_w2v_iter5.model') #学習済みモデル(wmDistance)
#wv = KeyedVectors.load_word2vec_format('./wiki.vec.pt', binary=True) #学習済みモデル(wmDistance)
print("LOAD SUCCESS")

#LOAD 発明効果 FILE
hatsumei = load_jsonfile("./out2/inv_filt_with_dist_after_discarding.json")
key_hatsu = hatsumei.keys()

#LOAD 実施例文 FILE
expermnt = load_jsonfile("./out/out-experiment.json")
key_exp = expermnt.keys()

all_res = []
shikiichi = 1.9

#FIND DISTANCE#
out = dict.fromkeys(key_hatsu)
out_inv = dict.fromkeys(key_hatsu)
out_exp = dict.fromkeys(key_hatsu)

for textfile in key_hatsu:
    if(hatsumei[textfile] == None or expermnt[textfile] == None):
        continue
    print(textfile)
    l1 = hatsumei[textfile]
    l2 = expermnt[textfile]
    res = []
    inv_true = set()
    exp_true = set()

    for word in l2:
        for word2 in l1:
            distance = wv.wmdistance(word,word2)
            if(distance >= shikiichi):
                continue
            tup_res = (word, word2, distance)
            res.append(tup_res)
            all_res.append(distance)
            inv_true.add(word2)
            exp_true.add(word)

    out[textfile] = res
    if(inv_true == {}):
        inv_true.add(0)
    out_inv[textfile] = list(inv_true)
    out_exp[textfile] = list(exp_true)

    out[textfile] = sorted(out[textfile], key=lambda x: x[2])


save_picklefile("all_res_distance_.lst", all_res)
save_jsonfile("distance_T.json", out)
save_jsonfile("all_koukago_from_hatsumei.json", out_inv)
save_jsonfile("all_koukago_from_jisshirei.json", out_exp)

print(len(all_res))