import regex as re

def discard_Katakana(dic):
    name_file = str(list(dic.keys())[0])
    value = list(dic.values())[0]

    new_value = []
    katakana_pattern = "\p{Katakana}"

    for word in value:
        total = len(re.findall(katakana_pattern, word))
        if (total <= 0):
            new_value.append(word)

    return {name_file : new_value}


#parameter list of word
def discard_Ascii(lis):

    new_value = []
    ascii_pattern = "[a-zA-Z0-9]"
    for word in lis:
        total = len(re.findall(ascii_pattern, word))
        if (total <= 0):
            new_value.append(word)

    return new_value

 #throw away word that you dont want#   
def discard_word(lis):

    new_value = []
    noword_pattern = "[(実.*)|(発.*)]"
    for word in lis:
        total = len(re.findall(noword_pattern, word))
        if (total <= 0):
            new_value.append(word)

    return new_value



def discard_setsuzoku(lis):

    new_value = []
    noword_pattern = "(そして)|(また)|(または)|(それに)|(さらに)|(したがって)"
    for word in lis:
        total = len(re.findall(noword_pattern, word))
        
        if (total <= 0):
            new_value.append(word)

    return new_value

if __name__ == '__main__':
    dic = {
        "1994096793.txt": [
        "真空度",
        "15型結晶構造",
        "合金材",
        "各々原料",
        "ニオブ原料",
        "真空引き",
        "ヘリウム雰囲気中",
        "PCT測定",
        "金属ニオブ",
        "15型立方晶合金",
        "放電容量",
        "溶解炉",
        "合金組成",
        "製造コスト",
        "放電特性"
    ]}

    x = discard_Ascii(dic)
    print(x)

