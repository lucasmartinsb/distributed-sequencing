import time
import sys
from calcula_similaridade import calcula_similaridade
import threading

def processa(sequencias_list, num_threads):
    tempo_inicio = time.time()

    # Dividir o trabalho entre as threads
    tamanho_sequencias = len(sequencias_list)
    tamanho_thread = tamanho_sequencias // num_threads

    threads = []
    resultados = []

    for i in range(num_threads):
        inicio = i * tamanho_thread
        fim = (i + 1) * tamanho_thread if i < num_threads - 1 else tamanho_sequencias
        thread = threading.Thread(target=acha_pares_similares, args=(sequencias_list, inicio, fim, resultados))
        threads.append(thread)
        thread.start()

    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()

    # Coletar os resultados de todas as threads
    pares_mais_similares_total = [resultado[0] for resultado in resultados]
    similaridade_total = [resultado[1] for resultado in resultados]

    # Encontrar o valor máximo da similaridade
    similaridade_maxima = max(similaridade_total)

    # Encontrar os índices dos pares que têm a maior similaridade
    similaridade_maxima_indice = [i for i, similaridade in enumerate(similaridade_total) if similaridade == similaridade_maxima]

    # Obter os pares correspondentes usando os índices encontrados
    pares_mais_similares_maximo = [par for i in similaridade_maxima_indice for par in pares_mais_similares_total[i]]

    tempo_fim = time.time()

    # Imprimir os resultados
    return f"""Sequências mais similares são {pares_mais_similares_maximo} com uma similaridade de {similaridade_maxima:.2%}\nTempo total de execução: {tempo_fim - tempo_inicio} segundos"""

def acha_pares_similares(sequencias, indice_inicio, indice_final, resultados):
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

    # Adicionar resultados à lista compartilhada
    resultados.append((pares_mais_similares, similaridade_maxima))

if __name__ == '__main__':
    arquivo_entrada = sys.argv[1]
    num_threads = sys.argv[2]
    sequencias_list = []

    with open(arquivo_entrada, 'r') as arquivo_entrada:
        for linha in arquivo_entrada:
            # Remove espaços em branco e caracteres de nova linha
            sequence = linha.strip()
            # Adiciona o item à lista
            sequencias_list.append(sequence)

    print(processa(sequencias_list=sequencias_list, num_threads=num_threads))
