import re
import neologdn
import spacy
from dictionary.IGNORE_WORDS import *
from mymodule.discardP import *
from mymodule.tools import *
from mymodule.findWords import *


nlp = spacy.load("ja_ginza")

def exct_experimental_section(doc):

    start   = 0
    end     = 0
    read    = 0
    pattern_start = re.compile("【実施例.*】|（実施例.*）")
    pattern_end  = re.compile("【発明.*】|（発明.*）|【図面の簡単な.*】")

    exp_texts = []

    for i, experiment in enumerate(doc):
        if(read == 0 and pattern_start.match(experiment) != None):   
            read = 1
            start = i
        if(read == 1 and pattern_end.match(experiment) != None):
            end = i
            break

    exp_texts = doc[start:end]

    for i in range(len(exp_texts)):
        exp_texts[i] = re.sub(r"【.*】|（.*） ?|〔[１２３４５６７８９０]?〕|<.*>|〈.*〉", "", exp_texts[i])
        exp_texts[i] = re.sub("\n| ?", "",exp_texts[i])
        exp_texts[i] = neologdn.normalize(exp_texts[i])

    while "" in exp_texts:
        exp_texts.remove("")

    return exp_texts

def exct_invention_section(doc):

    start   = 0
    end     = 0
    read    = 0
    pattern_start = re.compile("【発明の効果】|（発明の効果）")
    pattern_end  = re.compile("（図面の簡単な.*）|【図面の簡単な.*】| [-]*")
    
    exp_texts = []

    for i, experiment in enumerate(doc):
        if(read == 0 and pattern_start.match(experiment) != None):   
            read = 1
            start = i
            if (i == len(doc)-1): #IF 発明の効果 comes last 
                end = len(doc)
                break    
        if(read == 1 and pattern_end.match(experiment) != None):
            end = i
            break

    exp_texts = doc[start:end]

    for i in range(len(exp_texts)):
        exp_texts[i] = re.sub(r"【.*】|（.*） ?|〔[１２３４５６７８９０]?〕|<.*>|〈.*〉", "", exp_texts[i])
        exp_texts[i] = re.sub("\n| ?", "",exp_texts[i])
        exp_texts[i] = neologdn.normalize(exp_texts[i])

    while "" in exp_texts:
        exp_texts.remove("")

    exp_texts = delete_all_conclusion_word(exp_texts)
    return exp_texts

def delete_all_conclusion_word(inv_words):
    
    nlp = spacy.load("ja_ginza")
    matcher = Matcher()
    
    lis = []
    new_inventon_doc = []

    for inv_word in inv_words:

        sentences = re.split('。', inv_word)
        while "" in sentences:
            sentences.remove("")
        lis_split_by_dot = []
        
        for sentence in sentences:
            sentence = re.split('、', sentence)
            while "" in sentence:
                sentence.remove("")
            lis_split_by_comma = [] 
            
            for sent in sentence:
                doc = nlp(sent)
                found = matcher(doc)
            
                if len(found) <= 0:
                    lis_split_by_comma.append(sent)

                lis_split_by_comma = discard_setsuzoku(lis_split_by_comma)

            lis_split_by_comma = make_list_into_string(lis_split_by_comma, '、')           
            lis_split_by_dot.append(lis_split_by_comma)

        new_sentences = make_list_into_string(lis_split_by_dot, '。')
        new_inventon_doc.append(new_sentences)
    
    return new_inventon_doc

def clear_the_method_word(kakari_uke, bun_flag_found, bunsetsu):

    new_sent = ""
    noun_on_method_sent = []

    max_index = int(max(kakari_uke))
    ban_word_index = []

    for i in range(len(bun_flag_found)):
        if bun_flag_found[i] == 1:
            ban_word_index.append(i)

    for i in range(len(kakari_uke)):
        to_flag = check_kakari_uke(kakari_uke[i], kakari_uke, ban_word_index, bunsetsu, i, max_index)
        if to_flag != 1:
            new_sent += bunsetsu[i]
        else:
            doc = nlp(bunsetsu[i])
            res = find_noun_and_compound(doc, i)
            noun_on_method_sent.extend(res)
        

    #print(max_index, ban_word_index, type(ban_word_index))
    #print("LOAD ALL BUNSETU AFTER KAKARI UKE KAISEKI")
    #print(new_sent)

    return new_sent, noun_on_method_sent

def check_kakari_uke(main, kakari_uke, ban_word_index, bunsetsu, i, max_index):
    #print(bunsetsu[i] , bunsetsu[main])
    if main in ban_word_index:
        return 1
    elif main == max_index or main == kakari_uke[main]:
        return 0
    else:
        return check_kakari_uke(kakari_uke[main], kakari_uke, ban_word_index, bunsetsu, i, max_index)


