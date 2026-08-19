#  Mineração Textual e Processamento Concorrente na Pós-Graduação (CAPES/UFC)

Pipeline desenvolvido em Python puro para ingestão, agregação estatística, processamento de linguagem natural (NLP) e mineração textual com concorrência (**Multithreading**) sobre os dados da produção acadêmica da pós-graduação da **Universidade Federal do Ceará (UFC)**, oriundos da base oficial da **CAPES** (2021).

---

##  Sumário
- Visão Geral
- Arquitetura e Modularização
- Destaques de Engenharia e NLP
- Resultados e Métricas Extraídas
- Como Executar
- Estrutura do Repositório
- Autor

---

## Visão Geral

O projeto analisa um conjunto de **1.287 trabalhos acadêmicos** (teses e dissertações) defendidos nos programas de pós-graduação da UFC em 2021. A solução foi projetada sem o uso de frameworks pesados de dados (como Pandas), demonstrando domínio na manipulação de estruturas nativas em baixo nível, orientação a objetos, funções de alta ordem e concorrência multithread.

---

## Arquitetura e Modularização

O código adota o princípio de responsabilidade única (*Single Responsibility Principle*), dividindo a carga entre os seguintes módulos:

```text
┌────────────────────────────────────────────────────────┐
│               leitura.py (Ponto de Entrada)            │
└───────────────────────────┬────────────────────────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌─────────────────────┐
│classe_arquivo│    │ranking_top10 │    │ranking_palavras_    │
│(Ingestão CSV │    │(Agregações   │    │threads              │
│ & Objetos)   │    │ com Lambdas) │    │(NLP + Multithreading│
└──────────────┘    └──────────────┘    │ MapReduce)          │
                                        └─────────────────────┘
```

* **`classe_arquivo.py`:** Define a classe de domínio `Trabalho` e realiza o carregamento em streaming via `csv.DictReader`.
* **`ranking_top10.py`:** Implementa lógica de agregação genérica através de funções de alta ordem (*callbacks/lambdas*).
* **`ranking_palavras_threads.py`:** Executa o pipeline de sanitização/tokenização textual e realiza a contagem paralela por meio de threads nativas do Python.
* **`leitura.py`:** Orquestra a execução da CLI, validação de argumentos via `sys.argv` e exibição formatada dos resultados.

---

## Destaques de Engenharia e NLP

### 1. Processamento Concorrente com Padrão MapReduce
* **Particionamento em Shards:** A base de 1.287 registros é particionada em dois blocos equilibrados.
* **Mapeamento Paralelo (`threading.Thread`):** Duas threads executam simultaneamente (`t1.start()` e `t2.start()`), processando os blocos de forma isolada e sem contenção de *locks*.
* **Sincronização & Redução Global:** A função `soma_global` atua após o `join()`, consolidando os dicionários parciais em um resultado agregado unificado.

### 2. Pipeline de Processamento de Linguagem Natural (NLP)
* **Normalização Unicode (`NFKD`):** Desacoplamento e remoção de diacríticos e acentuações (`unicodedata`), garantindo que termos como `"produção"` e `"producao"` convirjam para o mesmo token.
* **Expressões Regulares (`re`):** Filtragem estrita de caracteres especiais e pontuações com `[^a-z0-9\s]`.
* **Stopwords Customizadas Bilíngues:** Remoção de mais de 200 palavras funcionais/vazias em Português e Inglês (artigos, preposições, pronomes, verbos auxiliares e marcadores discursivos).
* **Corte por Comprimento Semântico:** Descarte de tokens com 3 caracteres ou menos (`len(p) > 3`).

### 3. Funções de Alta Ordem e Reutilização
* A função `gerar_ranking_top10` recebe identificadores customizados via expressões `lambda` (ex.: `lambda t: t.programa` ou `lambda t: t.orientador`), evitando a duplicação de lógica para diferentes dimensões de agregação.

---

## Resultados e Métricas Extraídas

Execução com o dataset `ap2-capes-ufc-2021.csv`:

###  Top 5 Programas de Pós-Graduação com Maior Produção
| Posição | Programa de Pós-Graduação | Total de Trabalhos |
| :---: | :--- | :---: |
| **1º** | Economia | 61 |
| **2º** | Educação | 60 |
| **3º** | Letras | 58 |
| **4º** | Química | 42 |
| **5º** | Direito | 39 |

###  Top 5 Áreas de Conhecimento Combinadas
| Posição | Grande Área \| Área de Conhecimento | Total de Trabalhos |
| :---: | :--- | :---: |
| **1º** | Ciências Sociais Aplicadas \| Economia | 68 |
| **2º** | Lingüística, Letras e Artes \| Letras | 68 |
| **3º** | Ciências da Saúde \| Medicina | 65 |
| **4º** | Engenharias \| Engenharia Elétrica | 62 |
| **5º** | Ciências Humanas \| Educação | 60 |

###  Top 10 Palavras Mais Frequentes nos Títulos (Mineração via Threads)
| Posição | Termo Minerado | Ocorrências |
| :---: | :--- | :---: |
| **1º** | `analise` | 125 |
| **2º** | `avaliacao` | 103 |
| **3º** | `ceara` | 102 |
| **4º** | `estudo` | 97 |
| **5º** | `ensino` | 79 |
| **6º** | `brasil` | 68 |
| **7º** | `fortaleza` | 63 |
| **8º** | `saude` | 48 |
| **9º** | `efeito` | 46 |
| **10º** | `educacao` | 46 |

---

## Como Executar

### Pré-requisitos
* **Python 3.8+** instalado.
* O projeto utiliza exclusivamente módulos nativos da biblioteca padrão do Python (`csv`, `sys`, `threading`, `unicodedata`, `re`). Nenhuma dependência externa via `pip` é requerida.

### Execução via Terminal
```bash
python leitura.py ap2-capes-ufc-2021.csv
```

---

## Estrutura do Repositório

```text
├── ap2-capes-ufc-2021.csv         # Dataset oficial de produções CAPES/UFC 2021
├── classe_arquivo.py              # Ingestão de dados, modelagem de classes e stopwords
├── ranking_top10.py               # Agregações funcionais com lambdas
├── ranking_palavras_threads.py    # Pipeline de NLP e contagem paralela com Threads
├── leitura.py                     # Script principal de execução (CLI)
└── README.md                      # Documentação técnica do projeto
```

---

## Autor

**João Gabriel Aquino Ferreira**  
Graduando em Ciência de Dados — Universidade Federal do Ceará (UFC)  
* [LinkedIn](https://www.linkedin.com/in/jgabrielaquino)
* [GitHub](https://github.com/jgaquino24)
