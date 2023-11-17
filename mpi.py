from mpi4py import MPI
import time
import sys
from acha_pares_similares import acha_pares_similares_mpi

def processa(sequencias_list : list[str]):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    tempo_inicio = time.time()

    sequencias = []
    for sequencia in sequencias_list:
        sequencias.append(sequencia)

    # Distribuir o trabalho entre os processos
    tamanho_processo = len(sequencias) // size
    indice_inicio = rank * tamanho_processo
    indice_final = indice_inicio + tamanho_processo if rank < size - 1 else len(sequencias)

    pares_mais_similares_local, similaridade_local = acha_pares_similares_mpi(sequencias=sequencias, indice_inicio=indice_inicio, indice_final=indice_final)

    # Coletar os resultados de todos os processos
    pares_mais_similares_total = comm.gather(pares_mais_similares_local, root=0)
    similaridade_total = comm.gather(similaridade_local, root=0)

    if rank == 0:
        # Encontrar o valor máximo da similaridade
        similaridade_maxima = max(similaridade_total)

        # Encontrar os índices dos pares que têm a maior similaridade
        similaridade_maxima_indice = [i for i, similaridade in enumerate(similaridade_total) if similaridade == similaridade_maxima]

        # Obter os pares correspondentes usando os índices encontrados
        pares_mais_similares_maximo = [par for i in similaridade_maxima_indice for par in pares_mais_similares_total[i]]


        end = time.time()

        # Imprimir os resultados
        return f"""Sequências mais similares são {pares_mais_similares_maximo} com uma similaridade de {similaridade_maxima:.2%}\nTempo total de execução: {end - tempo_inicio} segundos"""
    else:
        return ""
# Exemplo de uso
if __name__ == "__main__":
    inFile = sys.argv[1]
    sequences_str = []
    with open(inFile,'r') as inputFile:
        for line in inputFile:
            # Remove espaços em branco e caracteres de nova linha
            sequence = line.strip()
            # Adiciona o item à lista
            sequences_str.append(sequence)
    resultado = processa(sequences_str)
    print(resultado)