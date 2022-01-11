import neologdn

from mymodule.findWords import * 
from dictionary.IGNORE_WORDS import *
from mymodule.tools import load_spacy


matcher = Matcher_Inv()

def find_noun_and_compound(doc, i):
    
    found_compound_noun = 0
    count = 0
    compound = ''
    maxword = len(doc)

    list_of_compound_word = set()
    """
    list_of_noun_word = set()
    list_all_words = set()
    """

    while True:
        
        
        try:    
            if(doc[count].pos_ == "NUM" and doc[count+1].dep_ == "compound"):
                compound += doc[count].text
                count += 1
        except IndexError:
            #print("Index out of limit! Line : " + str(i) + " 気にしないで")
            pass
    
        
        norm = neologdn.normalize(doc[count].norm_).isascii 
        while doc[count].dep_ == "compound" and doc[count].pos_ == "NOUN" and (norm != True):
            text = doc[count].text
            if (text in ig):
                break
            compound += text
            count += 1
            found_compound_noun = 1
        
        if(found_compound_noun == 1 and doc[count].pos_ == "NOUN"):
            if(doc[count].text in ig ):
                compound = ''
                found_compound_noun = 0                
            else :
                compound += doc[count].text
                found_compound_noun = 0
                list_of_compound_word.add(compound)
                #print(compound)
                compound = ""
       
        else:
            compound = ''
            found_compound_noun = 0
        
        """
        if(doc[count].pos_ == "NOUN" and found_compound_noun != 1):
            if(doc[count].text not in ig):
                list_of_noun_word.add(doc[count].text)
        """
        count += 1

        if(count == maxword):
            break
        
        
    """
    for word in list_of_compound_word:
        list_all_words.add(word)

    for word in list_of_noun_word:
        list_all_words.add(word)
    """

    list_of_compound_word = list(list_of_compound_word)

    """
    list_of_noun_word = list(list_of_noun_word)
    list_all_words = list(list_all_words)
    """

    return list_of_compound_word

def check_symbol(doc):
    for i in doc:
        pos = i.pos_
        if (pos == "SYM"):
            return True
    return False

def checkMethodWord(sentence):  
    nlp = load_spacy()
    sentence = nlp(sentence)
    matcher = Matcher_Inv()
    found = matcher(sentence)
    end = 0
    for id, s, e in found: 
        end = e

    

    if len(found) >= 1 :
        leftover_word = ""
        if(end != len(sentence)):
            for i in range(end, len(sentence)):
                leftover_word += str(sentence[i])
        
        if (leftover_word != ""):
            return 1, leftover_word   
        else:
            return 1, ""
    else:
        return 0, ""

    