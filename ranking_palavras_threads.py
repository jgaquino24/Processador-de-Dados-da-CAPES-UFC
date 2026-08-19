import re
import unicodedata
import threading

'''
==========================================
        Dados Stopwords
==========================================
'''
stopwords_pt = [
    # Artigos e contrações
    "a", "à", "as", "o", "os",
    "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas",
    "num", "numa", "nuns", "numas",
    "ao", "aos", "às",
    "pelo", "pela", "pelos", "pelas",
    "pro", "pra", "pros", "pras",
    "por",

    # Preposições
    "para", "pra", "com", "sem", "sob", "sobre",
    "entre", "até", "desde", "contra",
    "após", "antes", "depois", "durante",

    # Pronomes pessoais / objetos
    "eu", "tu", "ele", "ela", "nós", "vós",
    "eles", "elas", "você", "vocês",
    "me", "te", "se", "nos", "vos",
    "lhe", "lhes",

    # Pronomes possessivos
    "meu", "minha", "meus", "minhas",
    "teu", "tua", "teus", "tuas",
    "seu", "sua", "seus", "suas",
    "nosso", "nossa", "nossos", "nossas",

    # Demonstrativos
    "este", "esta", "estes", "estas",
    "esse", "essa", "esses", "essas",
    "aquele", "aquela", "aqueles", "aquelas",
    "isto", "isso", "aquilo",

    # Indefinidos / quantificadores
    "alguém", "ninguém", "algo",
    "todo", "toda", "todos", "todas",
    "muito", "muita", "muitos", "muitas",
    "pouco", "pouca", "poucos", "poucas",
    "mais", "menos",
    "cada", "algum", "alguma", "alguns", "algumas",
    "mesmo", "mesma", "mesmos", "mesmas",
    "outro", "outra", "outros", "outras",
    "tanto", "tanta", "tantos", "tantas",
    "qualquer", "nada", "tudo",

    # Pronomes relativos / interrogativos
    "que", "quem", "onde",
    "quando", "como", "qual", "quais",

    # Conjunções e partículas
    "e", "ou", "mas", "porém", "todavia", "contudo",
    "porque", "porquê", "pois", "portanto", "logo",
    "então", "também", "ainda", "já",
    "só", "nem", "se", "caso",

    # Advérbios e marcadores de tempo/lugar
    "aqui", "aí", "ali", "lá", "cá",
    "agora", "hoje", "ontem", "amanhã",
    "sempre", "nunca", "jamais",
    "talvez",

    # Verbos auxiliares / muito frequentes (formas comuns)
    "ser", "sou", "é", "era", "eram", "foi", "foram",
    "estar", "estou", "está", "estão", "estava", "estavam",
    "ter", "tenho", "tem", "têm", "tinha", "tinham",
    "haver", "há", "havia",
    "ir", "vou", "vai", "vão",
    "poder", "posso", "pode", "podem",
    "fazer", "faz", "fazem",

    # Negação e outros marcadores
    "não", "nao",
    "sim",
    "bem",
    "ok"
]

stopwords_en = [
    # Articles
    "a", "an", "the",

    # Pronouns
    "i", "me", "my", "mine", "myself",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself",
    "she", "her", "hers", "herself",
    "it", "its", "itself",
    "we", "us", "our", "ours", "ourselves",
    "they", "them", "their", "theirs", "themselves",

    # Demonstratives
    "this", "that", "these", "those",

    # Indefinite / quantifiers
    "all", "any", "both", "each", "either", "few",
    "many", "more", "most", "much",
    "neither", "no", "none",
    "some", "such", "several",
    "other", "others",
    "another",

    # Question words / relatives
    "who", "whom", "whose",
    "what", "which",
    "when", "where", "why", "how",

    # Prepositions
    "about", "above", "across", "after", "against",
    "along", "among", "around", "at",
    "before", "behind", "below", "beneath", "beside",
    "between", "beyond",
    "by", "despite", "down", "during",
    "except", "for", "from", "in", "inside", "into",
    "like", "near", "of", "off", "on", "onto", "outside",
    "over", "past", "since", "through", "throughout",
    "to", "toward", "under", "underneath",
    "until", "up", "upon", "with", "within", "without",

    # Conjunctions
    "and", "or", "but", "nor", "so", "yet",
    "although", "though", "even", "if", "unless",
    "because", "since", "while", "whereas",

    # Common adverbs / particles
    "again", "almost", "already", "also",
    "always", "never", "ever",
    "just", "only", "still", "yet",
    "too", "very", "rather", "quite",
    "here", "there",
    "then", "once",
    "now", "today", "yesterday", "tomorrow",

    # Auxiliaries and very frequent verbs (base + some forms)
    "am", "is", "are", "was", "were",
    "be", "been", "being",
    "have", "has", "had", "having",
    "do", "does", "did", "doing",
    "will", "would",
    "shall", "should",
    "can", "could",
    "may", "might",
    "must",

    # Other frequent verbs
    "get", "gets", "got", "gotten", "getting",
    "make", "makes", "made",
    "go", "goes", "went", "gone", "going",
    "know", "knows", "knew", "known",
    "say", "says", "said",
    "see", "sees", "saw", "seen",
    "come", "comes", "came",
    "take", "takes", "took", "taken",

    # Negation and polarity markers
    "not", "no", "nor",
    "don't", "doesn't", "didn't",
    "won't", "wouldn't",
    "can't", "couldn't",
    "shouldn't", "isn't", "aren't", "wasn't", "weren't",
    "haven't", "hasn't", "hadn't",

    # Fillers / discourse markers
    "also", "too",
    "really",
    "well",
    "okay", "ok",
    "etc"
]

stopwords = set(stopwords_pt + stopwords_en)

''''
==========================================
        Ranking de Palavras
==========================================
'''

def limpar_e_fatiar(titulo):
    if not titulo:
        return []
    
    '''transforma o texto em minúsculo'''
    texto = titulo.lower()
    
    '''descolar o acento da letra'''
    separa_letra_acento = unicodedata.normalize('NFKD', texto)

    '''descarta o acento e preserva apenas a letra'''
    texto_sem_acento = "".join(c for c in separa_letra_acento if not unicodedata.combining(c))
    
    '''remoção da pontuação (mantém apenas letras a - z, números 0 - 9 e espaços)'''
    texto_limpo = re.sub(r'[^a-z0-9\s]', ' ', texto_sem_acento)
    
    '''quebra o texto em uma lista por meio do split()'''
    fragmentacao = texto_limpo.split()

    '''filtra as palavras finais retirando as stopwords e as que possuem menos que 3 caracteres'''
    palavras_finais = list(filter(
        lambda p: p not in stopwords and len(p) > 3,
        fragmentacao                         
    ))
    return palavras_finais

class ThreadContagem(threading.Thread):
    def __init__(self, id_thread, lista_trabalhos):
        threading.Thread.__init__(self)
        self.id = id_thread
        self.dados = lista_trabalhos
        self.resultado_parcial = {}

    def run(self):
        print(f"[Thread {self.id}] Iniciada. Processando {len(self.dados)} itens")

        for trabalho in self.dados:
            palavras = limpar_e_fatiar(trabalho.titulo)

            for p in palavras:
                if p in self.resultado_parcial:
                    self.resultado_parcial[p] = self.resultado_parcial[p] + 1
                else:
                    self.resultado_parcial[p] = 1    

        print(f"[Thread {self.id}] Concluída.")    

def contagem_concorrente(todos_trabalhos):
    '''divisão em dois blocos, 
    do inicio ate a metade
    e da metade ate o final'''
    meio = len(todos_trabalhos) // 2
    bloco_1 = todos_trabalhos[:meio]
    bloco_2 = todos_trabalhos[meio:]  

    '''Threads'''
    t1 = ThreadContagem(1, bloco_1)
    t2 = ThreadContagem(2, bloco_2)

    '''inicialização'''
    t1.start()
    t2.start()

    '''término'''
    t1.join()
    t2.join()
        
    '''dicionario final que ira armazenar os resultados das duas threads'''
    contagem_global = {}

    def soma_global(dic_parcial):
        for palavra, quantidade in dic_parcial.items():
            if palavra in contagem_global:
                contagem_global[palavra] = contagem_global[palavra] + quantidade
            else:
                contagem_global[palavra] = quantidade

    soma_global(t1.resultado_parcial) 
    soma_global(t2.resultado_parcial) 

    return contagem_global
