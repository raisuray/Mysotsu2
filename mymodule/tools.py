import spacy


def make_list_into_string(lis, symbol):
    new_sentences = ""

    if symbol == '、':
        total = len(lis)
        for sentence in lis:
            if(total != lis.index(sentence)+1):
                new_sentences += sentence + symbol
            else:
                new_sentences += sentence

    if symbol == '。':
        for sentence in lis:
            new_sentences += sentence + symbol

    return new_sentences

def load_spacy():
    nlp = spacy.load("ja_ginza")
    return nlp