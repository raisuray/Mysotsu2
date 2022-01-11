from mymodule.Patent import Patent
from mymodule.findWords import *
from mymodule.discardP import *
from mymodule.myloader import *

import spacy

dict_eff_words = load_jsonfile("./template.json")
patents_list = load_picklefile("./patent_new.object")
outputfile_name = "out-invention-filterd.json"
ban_list_word = load_jsonfile("out2/listbannounwords.json")


#FIND ALL THE COMPOUND WORD IN ALL FILE#
nlp = spacy.load("ja_ginza")
for patent in patents_list:
    try:
        res = []
        list_of_compound_word = []
        print(patent.name)
        #print(len(patent.doc))

        for i in range(len(patent.new_doc_inv_word)):

            doc_samp = nlp(patent.new_doc_inv_word[i])
            if(check_symbol(doc_samp) == True and len(patent.new_doc_inv_word[i]) <= 10):
                continue
            list_of_compound_word = find_noun_and_compound(doc_samp, i)
            res.extend(list_of_compound_word)        
        res = list(set(res))
        res = discard_Ascii(res)
        res = discard_word(res)

        res = set(res)
        ban = set(ban_list_word[patent.name])

        res = res - ban

        dict_eff_words[patent.name] = list(res)
    except:
        with open("log.txt", "+a") as f:
            f.write(patent.name + " error ! \n")

#MAKE AN OUTPUT FILE#
path = "./out2/"
save_jsonfile(path + outputfile_name, dict_eff_words)


