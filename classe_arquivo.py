import csv

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

topwords = set(stopwords_pt + stopwords_en)


''''
==========================================
        Classe e Função (arquivo)
==========================================
'''

class Trabalho:
    def __init__(self, linha_csv):
        self.programa = linha_csv['NM_PROGRAMA']
        self.orientador = linha_csv['NM_ORIENTADOR']
        self.grande_area = linha_csv['NM_GRANDE_AREA_CONHECIMENTO']
        self.area_conhecimento = linha_csv['NM_AREA_CONHECIMENTO']
        self.titulo = linha_csv['NM_PRODUCAO']
        
        self.area_combinada = f"{self.grande_area} | {self.area_conhecimento}"
    def __repr__(self):
        return f"Trabalho: {self.titulo[:20]}...;"
    
def carregar_dados(caminho_do_arquivo):
    lista_de_trabalhos = []
    try:
        with open(caminho_do_arquivo, mode='r', encoding='utf-8') as arquivo:
            leitor_csv = csv.DictReader(arquivo, delimiter=';')
            for linha in leitor_csv:
                novo_trabalho = Trabalho(linha)
                lista_de_trabalhos.append(novo_trabalho)
        return lista_de_trabalhos  
          
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado!")
        return []
 
