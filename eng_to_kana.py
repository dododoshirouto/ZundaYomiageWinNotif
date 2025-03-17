# -*- coding: utf-8 -*-
"""
Morikatron Engineer Blog の記事 「英語をカタカナ表記に変換してみる」のサンプルコードです。詳しくは下記URLのブログ記事をご参照ください。
https://tech.morikatron.ai/entry/2020/05/25/100000

プログラムの実行にあたっては
http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b
http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/scripts/make_baseform.pl
上記の2つのファイルを本プログラムと同一ディレクトリにダウンロードして、
以下のコマンドを実行してください。
perl make_baseform.pl cmudict-0.7b cmudict-0.7b_baseform
これにより作成されるファイル　cmudict-0.7b_baseform　を本プログラムで読み込んで利用します。

本プログラムは python 3.4 以降で実行してください。
"""

import pathlib
import re


class EnglishToKana:

    def __init__(self, log=False):

        global log_text
        self.vowels = {
            'AA': '',  # 曖昧
            'AH': '',  # 曖昧
            'AE': 'a',
            'AO': 'o',
            'AW': 'a',
            'AY': 'a',
            'EH': 'e',
            'ER': 'a',
            'EY': 'e',
            'IH': 'i',
            'IY': 'i',
            'OW': 'o',
            'OY': 'o',
            'UH': 'u',
            'UW': 'u',
        }

        self.kana_dic = {
            'B': {'a': 'バ', 'i': 'ビ', 'u': 'ブ', 'e': 'ベ', 'o': 'ボ', '': 'ブ'},  # be	B IY
            'CH': {'a': 'チャ', 'i': 'チ', 'u': 'チュ', 'e': 'チェ', 'o': 'チョ', '': 'チ'},  # cheese	CH IY Z#チch
            'D': {'a': 'ダ', 'i': 'ディ', 'u': 'ドゥ', 'e': 'デ', 'o': 'ド', '': 'ド'},  # dee	D IY
            'DH': {'a': 'ザ', 'i': 'ジ', 'u': 'ズ', 'e': 'ゼ', 'o': 'ゾ', '': 'ズ'},  # thee	DH IY
            'F': {'a': 'ファ', 'i': 'フィ', 'u': 'フ', 'e': 'フェ', 'o': 'フォ', '': 'フ'},  # fee	F IY
            'G': {'a': 'ガ', 'i': 'ギ', 'u': 'グ', 'e': 'ゲ', 'o': 'ゴ', '': 'グ'},  # green	G R IY N
            'HH': {'a': 'ハ', 'i': 'ヒ', 'u': 'フ', 'e': 'ヘ', 'o': 'ホ', '': 'フ'},  # he	HH IY#H
            'JH': {'a': 'ジャ', 'i': 'ジ', 'u': 'ジュ', 'e': 'ジェ', 'o': 'ジョ', '': 'ジ'},  # gee	JH IY#J
            'K': {'a': 'カ', 'i': 'キ', 'u': 'ク', 'e': 'ケ', 'o': 'コ', '': 'ク'},  # key	K IY
            'L': {'a': 'ラ', 'i': 'リ', 'u': 'ル', 'e': 'レ', 'o': 'ロ', '': 'ル'},  # lee	L IY
            'M': {'a': 'マ', 'i': 'ミ', 'u': 'ム', 'e': 'メ', 'o': 'モ', '': 'ム'},  # me	M IY
            'N': {'a': 'ナ', 'i': 'ニ', 'u': 'ヌ', 'e': 'ネ', 'o': 'ノ', '': 'ン'},  # knee	N IY
            'NG': {'a': 'ンガ', 'i': 'ンギ', 'u': 'ング', 'e': 'ンゲ', 'o': 'ンゴ', '': 'ング'},  # ping	P IH NG
            'P': {'a': 'パ', 'i': 'ピ', 'u': 'プ', 'e': 'ペ', 'o': 'ポ', '': 'プ'},  # pee	P IY
            'R': {'a': 'ラ', 'i': 'リ', 'u': 'ル', 'e': 'レ', 'o': 'ロ', '': 'ー'},  # read	R IY D
            'S': {'a': 'サ', 'i': 'シ', 'u': 'ス', 'e': 'セ', 'o': 'ソ', '': 'ス'},  # sea	S IY
            'SH': {'a': 'シャ', 'i': 'シ', 'u': 'シュ', 'e': 'シェ', 'o': 'ショ', '': 'シュ'},  # she	SH IY
            'T': {'a': 'タ', 'i': 'ティ', 'u': 'チュ', 'e': 'テ', 'o': 'ト', '': 'ト'},  # tea	T IY
            'TH': {'a': 'サ', 'i': 'シ', 'u': 'シュ', 'e': 'セ', 'o': 'ソ', '': 'ス'},  # theta	TH EY T AH
            'V': {'a': 'バ', 'i': 'ビ', 'u': 'ブ', 'e': 'ベ', 'o': 'ボ', '': 'ブ'},  # vee	V IY
            'W': {'a': 'ワ', 'i': 'ウィ', 'u': 'ウ', 'e': 'ウェ', 'o': 'ウォ', '': 'ウ'},  # we	W IY
            'Y': {'a': 'ア', 'i': '', 'u': 'ュ', 'e': 'エ', 'o': 'ョ', '': 'イ'},  # yield	Y IY L D
            'BOS_Y': {'a': 'ヤ', 'i': 'イ', 'u': 'ユ', 'e': 'イエ', 'o': 'ヨ', '': 'イ'},
            'Z': {'a': 'ザ', 'i': 'ジ', 'u': 'ズ', 'e': 'ゼ', 'o': 'ゾ', '': 'ズ'},  # zee	Z IY
            'ZH': {'a': 'ジャ', 'i': 'ジ', 'u': 'ジュ', 'e': 'ジェ', 'o': 'ジョ', '': 'ジュ'},  # seizure	S IY ZH ER
            'T_S': {'a': 'ツァ', 'i': 'ツィ', 'u': 'ツ', 'e': 'ツェ', 'o': 'ツォ', '': 'ツ'},
        }

        if log:
            log_text = ''

        # 変換用辞書
        self.eng_kana_dic = {}

        # CMU辞書読み込み
        path_to_cmu = pathlib.Path(__file__).parent / './cmudict-0.7b_baseform'
        with open(path_to_cmu, 'r', encoding='us-ascii', errors='ignore') as f:
            lines = f.read().split('\n')
            for line in lines:
                if line == '':
                    continue
                word, p = line.split('\t')

                if not (0x41 <= ord(word[0]) <= 0x5a):
                    # アルファベット以外（記号とか）から始まる単語は無視
                    continue
                if '(' in word:
                    # '('を含む単語も無視　発音のバリエーションだから
                    continue
                word = word.lower()  # 小文字にしておく

                sound_list = p.split(' ')
                yomi = ''

                # EOS と BOS　をつけておく
                sound_list = ['BOS'] + sound_list + ['EOS']
                for i in range(1, len(sound_list) - 1):

                    s = sound_list[i]
                    s_prev = sound_list[i - 1]
                    s_next = sound_list[i + 1]

                    if s_prev == 'BOS' and s == 'Y':
                        # 頭がYの場合特殊
                        s = sound_list[i] = 'BOS_Y'

                    if s in self.kana_dic and s_next not in self.vowels:
                        # 子音(→子音）
                        if s_next in {'Y'}:
                            # 後ろが Y の場合イ行に
                            # ただし2文字の場合は2文字目を削る　例）フィ→フ
                            yomi += self.kana_dic[s]['i'][0]
                        elif s == 'D' and s_next == 'Z':
                            # D音をスキップ
                            continue
                        elif s == 'T' and s_next == 'S':
                            # 連結して'T_S'に
                            sound_list[i + 1] = 'T_S'
                            continue
                        elif s == 'NG' and s_next in {'K', 'G'}:
                            # 'NG'の次が 'G' or 'K' の場合2文字目を削る　例）ング→ン
                            yomi += self.kana_dic[s][''][0]
                        elif s_prev in {'EH', 'EY', 'IH', 'IY'} and s == 'R':
                            yomi += 'アー'
                        else:
                            yomi += self.kana_dic[s]['']
                    elif s in self.vowels:
                        # 母音
                        # aiueoに割り振る
                        if s in {'AA', 'AH'}:
                            # 曖昧母音
                            v = self.find_vowel(word, i - 1, len(sound_list) - 2)
                        else:
                            v = self.vowels[s]

                        if s_prev in self.kana_dic:
                            # (子音→)母音で
                            # print(s,v)
                            yomi += self.kana_dic[s_prev][v]
                        else:
                            # (母音→)母音
                            # 母音が連続すると変化するもの
                            if s_prev in {'AY', 'EY', 'OY'} and s not in {'AA', 'AH'}:  # 曖昧母音の場合は除外
                                yomi += {'a': 'ヤ', 'i': 'イ', 'u': 'ユ', 'e': 'エ', 'o': 'ヨ'}[v]
                            elif s_prev in {'AW', 'UW'}:
                                yomi += {'a': 'ワ', 'i': 'ウィ', 'u': 'ウ', 'e': 'ウェ', 'o': 'ウォ'}[v]
                            elif s_prev in {'ER'}:
                                yomi += {'a': 'ラ', 'i': 'リ', 'u': 'ル', 'e': 'レ', 'o': 'ロ'}[v]
                            else:
                                # 変化しない
                                yomi += {'a': 'ア', 'i': 'イ', 'u': 'ウ', 'e': 'エ', 'o': 'オ'}[v]

                        # Yを母音化
                        if s in {'AY', 'EY', 'OY'}:  # これは常に入れてOK?
                            yomi += 'イ'
                        # 後続が母音かどうかで変化するもの
                        if s_next not in self.vowels:
                            # 母音(→子音)
                            if s in {'ER', 'IY', 'OW', 'UW'}:
                                yomi += 'ー'
                            elif s in {'AW'}:
                                yomi += 'ウ'

                if log:
                    log_text += word + ' ' + yomi + ' ' + p + '\n'
                # 登録
                self.eng_kana_dic[word] = yomi

        if log:
            with open('log.txt', 'w') as f_out:
                f_out.write(log_text)

    # 表記から母音を取り出す関数（曖昧母音用）
    def find_vowel(self, text, pos, length):
        p = (pos + 0.5) / length
        lengthoftext = len(text)
        distance_list = []
        vowel_list = []
        for i, s in enumerate(text):
            if s in {'a', 'i', 'u', 'e', 'o'}:
                vowel_list.append(s)
                distance_list.append(abs(p - (i + 0.5) / lengthoftext))
        if len(distance_list) == 0:
            # 母音が無い
            return 'a'
        v = vowel_list[distance_list.index(min(distance_list))]
        # uはaに置き換える
        if v == 'u':
            v = 'a'
        return v
    
    ing_fix_ja_dic = {
        's' : 'ズ',
        'd' : 'ド',
        'es' : 'ズ',
        'ed' : 'ド',
    }

    def convert(self, english):
        english = english.lower()
        if english in self.eng_kana_dic:
            return self.eng_kana_dic[english]
        else:
            # print (f'ERROR 辞書にありません -> {english}')

            fix = english[-2:]
            fix_ja = ''
            if fix in self.ing_fix_ja_dic:
                fix_ja = self.ing_fix_ja_dic[fix]
                if english[:-2] in self.eng_kana_dic:
                    return self.eng_kana_dic[english[:-2]] + fix_ja
                
            fix = english[-1:]
            fix_ja = ''
            if fix in self.ing_fix_ja_dic:
                fix_ja = self.ing_fix_ja_dic[fix]
                if english[:-1] in self.eng_kana_dic:
                    return self.eng_kana_dic[english[:-1]] + fix_ja
                
            print (f'ERROR 辞書にありません -> {english}')
            return english
    
    # dododo-shirouto 英日混在に対応
    def convertsZakkuri(self, texts):
        """英日混在テキストをカタカナに変換"""
        tokens = re.findall(r"[a-zA-Z']+|[^a-zA-Z']+", texts)

        result = []
        for token in tokens:
            if re.match(r"[a-zA-Z']+", token):  # 英語なら変換
                result.append(self.convert(token))
            else:  # 日本語なら OpenJTalk で変換
                result.append(token)

        return "".join(result)



if __name__ == "__main__":
    e2k = EnglishToKana()
    print(e2k.convertsZakkuri("""Where creatives get their news 📰 

- 5 free tools, resources, and tutorials every single week.
- The latest updates and news on creative tools.
- 100% free, unsubscribe anytime.

Subscribe here"""))