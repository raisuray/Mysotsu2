from mymodule.myloader import * 
from mymodule.findWords import *
from mymodule.extract import clear_the_method_word
import numpy as np
import CaboCha

cp = CaboCha.Parser()

def gen_chunks(tree):
    """
    構文木treeからチャンクの辞書を生成する
    """
    chunks = {}
    key = 0  # intにしているがこれはChunk.linkの値で辿れるようにしている

    for i in range(tree.size()):  # ツリーのサイズだけ回す
        tok = tree.token(i)  # トークンを得る
        if tok.chunk:  # トークンがチャンクを持っていたら
            chunks[key] = tok.chunk  # チャンクを辞書に追加する
            key += 1

    return chunks

def get_surface(tree, chunk):
    """
    chunkからtree内のトークンを得て、そのトークンが持つ表層形を取得する
    """
    surface = ''
    beg = chunk.token_pos  # このチャンクのツリー内のトークンの位置
    end = chunk.token_pos + chunk.token_size  # トークン列のサイズ
    for i in range(beg, end):
        token = tree.token(i)
        surface += token.surface  # 表層形の取得

    return surface

# parm     = 発明の効果文
# return   = 係り受け解析行った発明の効果文を返す
def deletehousent(inv_word, name):
    
    new_sentence_list = []

    for word in inv_word:

        new_sentence = ""
    
        bunsetsu_T = []
        bunsetsu = []

        sentence = word
        cp = CaboCha.Parser()  # パーサーを得る
        tree = cp.parse(sentence)  # 入力から構文木を生成
        print(tree.toString(CaboCha.FORMAT_TREE))  # デバッグ用

        chunks = gen_chunks(tree)  # チャンクの辞書を生成する

        for from_chunk in chunks.values():
            if from_chunk.link < 0:
                continue  # リンクのないチャンクは飛ばす

            # このチャンクの表層形を取得
            from_surface = get_surface(tree, from_chunk)

            # from_chunkがリンクしているチャンクを取得
            to_chunk = chunks[from_chunk.link]
            to_surface = get_surface(tree, to_chunk)
            # 出力
            # print(from_surface, '->', to_surface)
            
            bunsetsu.append(from_surface)
            bunsetsu_T.append((from_surface,to_surface))

        bunsetsu.append(to_surface)
        bunsetsu_T.append(("",to_surface))

        # Make flag found for bunsetsu list and kakari uke list 
        # number on bun_flag_found means index of bunsetsu
        kakari_uke = np.zeros(len(bunsetsu_T), np.int8())
        bun_flag_found = np.zeros(len(bunsetsu_T), np.int8())

        for i in range(len(bunsetsu_T)):
            kakari_uke[i] = bunsetsu.index(bunsetsu_T[i][1], i)

        for i in range(len(bunsetsu)):
           
            flag, leftword = checkMethodWord(bunsetsu[i])
            if (flag == 1):
                if (leftword != ""):
                    bunsetsu[i] = leftword
                bun_flag_found[i] = 1


        new_sent, noun_on_method_sent = clear_the_method_word(kakari_uke, bun_flag_found, bunsetsu)
        new_sentence_list.append(new_sent)
        f[name] = noun_on_method_sent
        save_jsonfile("./listbannounwords.json" , f)

    return new_sentence_list


### extract noun word in method sentence -> listbannounword.json
### add another field into PatentClass in patent_new.object 
patent_list = load_picklefile("patent.object")
f = load_jsonfile("template.json")

for patent in patent_list:
    try:
        print(patent.name, patent.doc_invention)

        new = deletehousent(patent.doc_invention, patent.name)   
        patent.new_doc_inv_word = new
        save_picklefile("./patent_new.object", patent_list)

        print(patent.name, new)
        print("-"*16)

    except:
        with open("log.txt", "+a") as f:
            f.write(patent.name + " error ! \n")

print("CLEAR")

"""
patent = patent_list[3]
print(patent.name, patent.doc_invention)
new = deletehousent(patent.doc_invention, patent.name)   
print(new)
patent.new_doc_inv_word = new

"""