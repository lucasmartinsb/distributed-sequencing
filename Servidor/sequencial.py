import time
import sys
from calcula_similaridade import calcula_similaridade

def processa(sequencias_list : list):
    tempo_inicio = time.time()
    
    # Encontrar os pares mais similares e a similaridade geral
    pares_mais_similares, similaridade = acha_pares_similares(sequencias_list)
    
    tempo_fim = time.time()
    
    return {
        'Pares' : pares_mais_similares,
        'Similaridade' : f"{similaridade:.2%}",
        'Tempo' : tempo_fim - tempo_inicio
    } 

def acha_pares_similares(sequencias):
    quant_sequencias = len(sequencias)
    pares_mais_similares = []
    similaridade_maxima = 0

    for i in range(quant_sequencias):
        for j in range(i + 1, quant_sequencias):
            similaridade = calcula_similaridade(sequencias[i], sequencias[j])
            if similaridade > similaridade_maxima:
                similaridade_maxima = similaridade
                pares_mais_similares = [(i, j)]
            elif similaridade == similaridade_maxima:
                pares_mais_similares.append((i, j))

    return pares_mais_similares, similaridade_maxima

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