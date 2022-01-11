from mymodule.myloader import  * 
import regex as re
import sys
import CaboCha
import spacy
import numpy as np

cp = CaboCha.Parser()
nlp = spacy.load('ja_ginza')

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



koukago_inv = load_jsonfile("all_koukago_from_hatsumei.json")
koukago_exp = load_jsonfile("all_koukago_from_jisshirei.json")
patent_list =  load_picklefile("patent_new.object")

patent_name =  list(koukago_exp.keys())

name = input("特許文書のファイル名前を入力してください = ")

if name not in patent_name:
    print("ファイルはありません")
    sys.exit()

koukago_inv = koukago_inv[name]
koukago_exp = koukago_exp[name]

for p in range(len(patent_list)):
    if patent_list[p].name == name:
        patent = patent_list[p]


print(patent.name)
print("実施例にある効果語らしい = ", koukago_exp)
print("発明の効果の効果語       = ", koukago_inv)

    
new_sentence_list = []
for sentence in patent.new_doc_inv_word:
    print(sentence)
    
    new_sentence = []

    bunsetsu_T = []
    bunsetsu = []
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
        print(from_surface, '->', to_surface)
        bunsetsu.append(from_surface)
        bunsetsu_T.append((from_surface,to_surface))
    
    bunsetsu.append(to_surface)
    bunsetsu_T.append(("",to_surface))

    #print(bunsetsu)
    #print(bunsetsu_T)

    kakari_uke = np.zeros(len(bunsetsu_T), np.int8())
    for i in range(len(bunsetsu_T)):
        kakari_uke[i] = bunsetsu.index(bunsetsu_T[i][1], i)

    for i in range(len(kakari_uke)):
        flag = i
        temp = ''
        
        while flag < len(kakari_uke)-1:
            temp += bunsetsu[flag]
            flag = kakari_uke[flag]
        temp += bunsetsu[-1]
        new_sentence.append(temp)

    for word in koukago_inv:
        for sent in new_sentence:
            print(len(re.findall(word,sent)))
            if (len(re.findall(word,sent)) != 0):
                print(sent)