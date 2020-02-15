import pandas as pd
import re

""" Patterns """
letter_and_number = re.compile(r'[A-Z]\d')
plus = re.compile(r'\(\+[\+]+\)')
spaces = re.compile(r'($|\w)\s{2,}')
hifen = re.compile(r'\d[\-]+\d')
spaces_bf_qual = re.compile(r'[A-Z][\s]+\_')
spaces_bf_dir = re.compile(r'[A-Z][\s]+\_\d')
add_space_left_qual = re.compile(r'\d[A-Z]\_[A-Z]')
space_btw_name_and_par = re.compile(r'[A-Z][\s]+\([\+\-]')
nao_space_underline = re.compile(r'NÃO\s')
famoso_famosa = re.compile(r'_(FAMOSO|FAMOSA)')
not_decimal_dot = re.compile(r'\.+(\D|$)')
imp_zero = re.compile(r'(^|\s)\.\d')


""" Ler csv e tratar ocorrências"""
corpus = pd.read_csv('corpus-q1-v2.csv')


#print("Process Start...")
for i in range(corpus.shape[0]):
    """
    if i == (corpus.shape[0]//4):
        print("25%...")
    if i == (corpus.shape[0]//2):
        print("50%...")
    if i == ((corpus.shape[0]*3)//4):
        print("75%...")
"""
    # procurar letra seguida de número (apenas em gi dado que o padrão digito->letra não se encontra em gr)
    """okok"""
    matches = letter_and_number.finditer(corpus['gi'][i])
    for match in matches:
        # transforma a string em lista para trocar as ocorrências erradas
        lst = list(corpus['gi'][i])
        lst[ match.span()[0] ], lst[ match.span()[1] - 1 ] = lst[ match.span()[1] - 1 ], lst[ match.span()[0] ]
        corpus['gi'][i] = ''.join(lst)

        
    # procurar ocorrência de múltiplos + dentro de parênteses
    """okok"""
    matches = plus.finditer(corpus['gr'][i]) # em gr
    offset = 0 
    # offset corrige a posição em relação ao spam depois de remover a primeira ocorrência (ao criar
    # uma nova string com tamanho reduzido, não se pode mais considerar os indices encontrados anteriormente)
    for match in matches:
        corpus['gr'][i] = corpus['gr'][i][:match.span()[0]+2-offset] + corpus['gr'][i][match.span()[1]-1-offset:]
        offset += match.span()[1] - match.span()[0] - 2
        
    matches = plus.finditer(corpus['gi'][i]) # em gi
    offset = 0
    for match in matches:
        corpus['gi'][i] = corpus['gi'][i][:match.span()[0]+2-offset] + corpus['gi'][i][match.span()[1]-1-offset:]
        offset += match.span()[1] - match.span()[0] - 2

        
    # procurar ocorrência de múltiplos espaços
    """não"""
    matches = spaces.finditer(corpus['gr'][i]) # em gr
    offset = 0
    for match in matches:
        corpus['gr'][i] = corpus['gr'][i][:match.span()[0]+1-offset]+ corpus['gr'][i][match.span()[1]-1-offset:]
        offset += match.span()[1] - match.span()[0] - 2
    
    matches = spaces.finditer(corpus['gi'][i]) # em gi
    offset = 0
    for match in matches:
        corpus['gi'][i] = corpus['gi'][i][:match.span()[0]+1] + corpus['gi'][i][match.span()[1]-1:]
        offset += match.span()[1] - match.span()[0] - 1
        
    
    # procurar hífen entre digitos
    """okok"""
    matches = hifen.finditer(corpus['gr'][i]) # em gr
    offset = 0
    for match in matches:
        corpus['gr'][i] = corpus['gr'][i][:match.span()[0]+1-offset] + corpus['gr'][i][match.span()[1]-1-offset:]
        offset += match.span()[1] - match.span()[0] - 2
    
    matches = hifen.finditer(corpus['gi'][i]) # em gi
    offset = 0
    for match in matches:
        corpus['gi'][i] = corpus['gi'][i][:match.span()[0]+1-offset] + corpus['gi'][i][match.span()[1]-1-offset:]
        offset += match.span()[1] - match.span()[0] - 2
        
    
    # procurar por espaços incorretamente inseridos (só acontece o padrão "nome_nome" em gi)
    """okok"""
    matches = spaces_bf_qual.finditer(corpus['gr'][i]) # em gr
    offset = 0
    for match in matches:
        corpus['gr'][i] = corpus['gr'][i][:match.span()[0]+1-offset] + corpus['gr'][i][match.span()[1]-1-offset:]
        offset += match.span()[1] - match.span()[0] - 2

    
    matches = spaces_bf_qual.finditer(corpus['gi'][i]) # em gi
    offset = 0
    for match in matches:
        corpus['gi'][i] = corpus['gi'][i][:match.span()[0]+1-offset] + corpus['gi'][i][match.span()[1]-1-offset:]
        offset += match.span()[1] - match.span()[0] - 2
        
    
    # procurar espaços incorretamente inseridos antes de qualificadores direcionais na direita (só é possível 
    # encontrar esse padrão em gi)
    """okok"""
    matches = spaces_bf_dir.finditer(corpus['gi'][i]) # em gi
    offset = 0
    for match in matches:
        corpus['gi'][i] = corpus['gi'][i][:match.span()[0]+1-offset] + corpus['gi'][i][match.span()[1]-2-offset:]
        offset += match.span()[1] - match.span()[0] - 3
        
    
    # Adicionar espaços após os qualificadores direcionais pela esquerda
    """okok"""
    matches = add_space_left_qual.finditer(corpus['gi'][i]) # novamente apenas em gi
    offset = 0
    for match in matches:
        corpus['gi'][i] = corpus['gi'][i][:match.span()[0]+3-offset] + " " + corpus['gi'][i][match.span()[1]-1-offset:]
        offset -= 1
        

    # Remova os espaços à esquerda dos qualificadores de intensidade
    """okok"""
    matches = space_btw_name_and_par.finditer(corpus['gr'][i]) # em gr
    offset = 0
    for match in matches:
        corpus['gr'][i] = corpus['gr'][i][:match.span()[0]+1-offset] + corpus['gr'][i][match.span()[1]-2-offset:]
        offset += 1
        
    matches = space_btw_name_and_par.finditer(corpus['gi'][i]) # em gi
    offset = 0
    for match in matches:
        corpus['gi'][i] = corpus['gi'][i][:match.span()[0]+1-offset] + corpus['gi'][i][match.span()[1]-2-offset:]
        offset += 1
        
    
    # substituir espaço por _ depois do NÃO
    """okok"""
    matches = nao_space_underline.finditer(corpus['gr'][i]) # em gr
    for match in matches:
        corpus['gr'][i] = corpus['gr'][i][:match.span()[0]+3] + "_" + corpus['gr'][i][match.span()[1]:]
                
    matches = nao_space_underline.finditer(corpus['gi'][i]) # em gi
    for match in matches:
        corpus['gi'][i] = corpus['gi'][i][:match.span()[0]+3] + "_" + corpus['gi'][i][match.span()[1]:]
        
        
    # substituir sublinha por & antes de famoso/famosa (pelo padrão, só necessário verificar gi)
    """okok"""
    matches = famoso_famosa.finditer(corpus['gi'][i])
    for match in matches:
        corpus['gi'][i] = corpus['gi'][i][:match.span()[0]]+ "&" + corpus['gi'][i][match.span()[1]-6:]
        
    
    # retirar pontos de não decimais
    """okok"""
    matches = not_decimal_dot.finditer(corpus['gr'][i]) # em gr
    offset = 0
    for match in matches:
        if match.span()[1] == len(corpus['gr'][i]): # ponto no fim
            corpus['gr'][i] = corpus['gr'][i][:-(match.span()[1]-match.span()[0])]
        else:
            corpus['gr'][i] = corpus['gr'][i][:match.span()[0]-offset] + corpus['gr'][i][match.span()[1]-1-offset:]
            offset += match.span()[1]-match.span()[0]-1
    
    matches = not_decimal_dot.finditer(corpus['gi'][i]) # em gi
    offset = 0
    for match in matches:
        if match.span()[1] == len(corpus['gi'][i]): # ponto no fim
            corpus['gi'][i] = corpus['gi'][i][:-(match.span()[1]-match.span()[0])]
        else:
            corpus['gi'][i] = corpus['gi'][i][:match.span()[0]-offset] + corpus['gi'][i][match.span()[1]-1-offset:]
            offset += match.span()[1]-match.span()[0]-1
        
    
    # adicionar zero implicito em decimais
    """okok"""
    matches = imp_zero.finditer(corpus['gr'][i]) # em gr
    offset = 0
    for match in matches:
        if match.span()[0] == 0: # ponto no inicio
            corpus['gr'][i] = '0' + corpus['gr'][i][match.span()[1]-2-offset:]
        else:
            corpus['gr'][i] = corpus['gr'][i][:match.span()[0]+1-offset] + '0' + corpus['gr'][i][match.span()[1]-2-offset:]
            offset -= 1
        
    matches = imp_zero.finditer(corpus['gi'][i]) # em gi
    offset = 0
    for match in matches:
        if match.span()[0] == 0:
            corpus['gi'][i] = '0' + corpus['gi'][i][match.span()[1]-2-offset:] # ponto no inicio
        else:
            corpus['gi'][i] = corpus['gi'][i][:match.span()[0]+1-offset] + '0' + corpus['gi'][i][match.span()[1]-2-offset:]
            offset -= 1


corpus.to_csv("corpus-resposta-1.csv")
# print("Process Finished...")