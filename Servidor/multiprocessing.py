import time
import sys
from calcula_similaridade import calcula_similaridade
from multiprocess import Pool

def processa(sequencias_list):
    tempo_inicio = time.time()

    # Distribuir o trabalho entre os processos
    tamanho_processo = len(sequencias_list) // num_processos
    resultados = []

    with Pool(processes=num_processos) as pool:
        resultados = pool.starmap(acha_pares_similares, [(sequencias_list, i, i + tamanho_processo) for i in range(0, len(sequencias_list), tamanho_processo)])

    # Coletar os resultados de todos os processos
    pares_mais_similares_total = [resultado[0] for resultado in resultados]
    similaridade_total = [resultado[1] for resultado in resultados]

    # Encontrar o valor máximo da similaridade
    similaridade_maxima = max(similaridade_total)

    # Encontrar os índices dos pares que têm a maior similaridade
    similaridade_maxima_indice = [i for i, similaridade in enumerate(similaridade_total) if similaridade == similaridade_maxima]

    # Obter os pares correspondentes usando os índices encontrados
    pares_mais_similares_maximo = [par for i in similaridade_maxima_indice for par in pares_mais_similares_total[i]]

    tempo_fim = time.time()

    return {
        'Pares' : pares_mais_similares_maximo,
        'Similaridade' : f"{similaridade_maxima:.2%}",
        'Tempo' : tempo_fim - tempo_inicio
    }
    
def acha_pares_similares(sequencias, indice_inicio, indice_final):
    quant_sequencias = len(sequencias)
    pares_mais_similares = []
    similaridade_maxima = 0

    for i in range(indice_inicio, indice_final):
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
    num_processos = int(sys.argv[2])
    sequencias_list = []
    with open(arquivo_entrada, 'r') as arquivo_entrada:
        for linha in arquivo_entrada:
            # Remove espaços em branco e caracteres de nova linha
            sequence = linha.strip()
            # Adiciona o item à lista
            sequencias_list.append(sequence)
    print(processa(sequencias_list=sequencias_list))