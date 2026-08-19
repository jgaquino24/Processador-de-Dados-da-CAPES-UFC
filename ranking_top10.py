''''
==========================================
        Ranking Top 10
==========================================
'''

def gerar_ranking_top10(lista_trabalhos, identificador):
    valores = [identificador(t) for t in lista_trabalhos]
    contagem = {}

    for item in valores:
        if item in contagem:
            contagem[item] = contagem[item] + 1
        else:
            contagem[item] = 1

    '''Transfomar o dicionario em uma lista para ppoder utilizar o sorted'''        
    lista_contagem = list(contagem.items())  

    '''Sorted para organizar; 
    x[1] serve para usar o número como o parametro a ser seguido na ordenação;
    reverse=True serve para que a ordenaçao seja do maior para o menor, 
    tendo em vista que o sorted organiza do menor para o maior'''
    ranking_ordenado = sorted(lista_contagem, key = lambda x: x[1], reverse=True)

    return ranking_ordenado[:10]     
