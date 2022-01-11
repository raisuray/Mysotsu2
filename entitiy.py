import spacy
import os 
from mymodule.myloader import *

dict_eff_words = load_jsonfile("./out2/inv_filt_with_dist_after_discarding.json")

path = './effect_words/'
effect_words = os.listdir(path)
res = dict.fromkeys(effect_words)


nlp = spacy.load("ja_ginza")

for patent_name in effect_words:

    if (dict_eff_words[patent_name] != None):
        temp = []
        for word in dict_eff_words[patent_name]:
            
            doc = nlp(word)
            for entitiy in doc.ents:
                if(entitiy.label_ == "Doctrine_Method_Other"):
                    continue
                print(entitiy.text , "->" , entitiy.label_) 
                temp.append(entitiy.text)

        res[patent_name] = temp                
        
save_jsonfile("./out2/inv_filt_with_dist_after_discarding_and_entity.json", res)