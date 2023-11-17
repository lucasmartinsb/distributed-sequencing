import warnings
warnings.filterwarnings("ignore")
import time
import sys
from acha_pares_similares import acha_pares_similares_sequencial

def processa(sequencias_list : list):
    tempo_inicio = time.time()
    
    # Encontrar os pares mais similares e a similaridade geral
    pares_mais_similares, similaridade = acha_pares_similares_sequencial(sequencias_list)
    
    tempo_fim = time.time()
    
    # Imprimir os resultados
    return (f"Sequências mais similares são {pares_mais_similares} com uma similaridade de {similaridade:.2%}.", tempo_fim - tempo_inicio)

if __name__ == '__main__':
    arquivo_entrada = sys.argv[1]
    sequencias_list = []
    with open(arquivo_entrada,'r') as arquivo_entrada:
        for linha in arquivo_entrada:
            # Remove espaços em branco e caracteres de nova linha
            sequence = linha.strip()
            # Adiciona o item à lista
            sequencias_list.append(sequence)
    print(processa(sequencias_list=sequencias_list))