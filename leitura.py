import sys
from classe_arquivo import carregar_dados
from ranking_top10 import gerar_ranking_top10
from ranking_palavras_threads import contagem_concorrente

''''
==========================================
        Execução (main)
==========================================
'''
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro: é necessário informar o caminho do arquivo CSV")
        print("Exemplo de uso: python caminho_arquivo.py caminho_para_dataset.csv")
        sys.exit(1)    
    
    caminho_do_arquivo = sys.argv[1]
    print(f"Iniciando processamento do arquivo: {caminho_do_arquivo}")

    meus_dados = carregar_dados(caminho_do_arquivo)
    print(f"Sucesso! Foram carregados {len(meus_dados)} trabalhos")
  
    if meus_dados:
        print("\n" + "="*40)
        print("REQUISITO 2: TOP 10 PROGRAMAS")
        print("="*40)
        ranking_programas = gerar_ranking_top10(meus_dados, lambda t: t.programa)
        i = 1
        for nome, quantidade in ranking_programas:
            print(f" {i}. {quantidade} trabalhos - {nome}")
            i = i + 1
        
        print("\n" + "="*40)
        print("REQUISITO 3: TOP 10 ORIENTADORES")
        print("="*40)
        ranking_orientadores = gerar_ranking_top10(meus_dados, lambda t: t.orientador)
        i = 1
        for nome, quantidade in ranking_orientadores:
            print(f" {i}. {quantidade} trabalhos - {nome}")
            i = i + 1

        print("\n" + "="*40)
        print("REQUISITO 4: TOP 10 ÁREAS COMBINADAS")
        print("="*40)
        ranking_areas_combinadas = gerar_ranking_top10(meus_dados, lambda t: t.area_combinada)
        i = 1
        for nome, quantidade in ranking_areas_combinadas:
            print(f" {i}. {quantidade} trabalhos - {nome}")
            i = i + 1  

        print("\n" + "="*40)
        print("REQUISITO 5: TOP 2O PALAVRAS(THREADS)")
        print("="*40)    
        '''executa as threads e pega o dicionario somado fornecido'''
        dict_palavras = contagem_concorrente(meus_dados)

        '''transforma o dicionario em lista para realizar a ordenação'''
        lista_palavras = list(dict_palavras.items())

        '''Sorted para organizar; 
        x[1] serve para usar o número como o parametro a ser seguido na ordenação;
        reverse=True serve para que a ordenaçao seja do maior para o menor, 
        tendo em vista que o sorted organiza do menor para o maior'''
        ranking_palavras = sorted(lista_palavras, key= lambda x: x[1], reverse= True)

        i = 1
        for palavra, quantidade in ranking_palavras[:20]:
            print(f" {i}. {quantidade} ocorrências - {palavra}")
            i = i + 1
