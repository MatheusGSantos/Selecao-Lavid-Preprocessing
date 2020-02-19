import pandas as pd
import re

""" Patterns """
patterns = {
    r'(?P<letter>(S|P))(?P<number>(1|2|3))':r'\g<number>\g<letter>', # S1 -> 1S
    r'(?<=\()\++(?=\))':"+", # (++) -> (+)
    r'\s+':" ", # "  " -> " "
    r'(?<=\d)\-+(?=\d)':'', # 123-456 -> 123456
    r'\s+(?=(_CIDADE|_ESTADO|_PAÍS))':"", # retira espaços antes de qualificadores de "_local"
    r'(?<=[A-Z])\s+_(?=\d)':"_", # 1S_AMAR _2S -> 1S_AMAR_2S
    r'(?<=\d(S|P))_(?=[A-Z])':"_ ", # 1S_DAR_3P -> 1S_ DAR_3P
    r'(?<=[A-Z])\s+(?=\((\+|\-))':"", # AMAR (+) -> AMAR(+)
    r'(?<=NÃO)\s+':"_", # NÃO ENCONTRADO -> NÃO_ENCONTRADO
    r'_+(?=(FAMOSO|FAMOSA))':"&", # _FAMOSO -> &FAMOSO
    r'(?<=\D)?\.+(?=(\D|$))':"", # remove ponto não decimal (trata início, entre letras e/ou espaços e fim)
    r'(?<=\s)?\.(?=\d)':"0." # acrescenta 0 implicito
    }


""" Ler csv"""
corpus = pd.read_csv('corpus-q1-v2.csv')


print("Process Start...")

def df_correction(df):
    for col in df.columns:
        print(f'Start {col}...')
        size = len(df[col])
        col_pos = df.columns.get_loc(col)
        for ind in range(size):
            for p in patterns:
                df.iat[ind, col_pos] = re.sub(p, patterns[p], df.iat[ind, col_pos])

        print(f'Finished {col}...')
        


df_correction(corpus)
corpus.to_csv("corpus-resposta-1.csv")

print("Process Finished...")