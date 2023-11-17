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
    chunk_size = len(sequencias) // size
    start_index = rank * chunk_size
    end_index = start_index + chunk_size if rank < size - 1 else len(sequencias)

    local_most_similar_pairs, local_max_similarity = acha_pares_similares_mpi(sequencias, start_index, end_index)

    # Coletar os resultados de todos os processos
    all_most_similar_pairs = comm.gather(local_most_similar_pairs, root=0)
    all_max_similarity = comm.gather(local_max_similarity, root=0)

    if rank == 0:
        # Encontrar o valor máximo da similaridade
        max_similarity = max(all_max_similarity)

        # Encontrar os índices dos pares que têm a maior similaridade
        max_similarity_indices = [i for i, similarity in enumerate(all_max_similarity) if similarity == max_similarity]

        # Obter os pares correspondentes usando os índices encontrados
        max_similarity_pairs = [pair for i in max_similarity_indices for pair in all_most_similar_pairs[i]]


        end = time.time()

        # Imprimir os resultados
        return f"""Sequências mais similares são {max_similarity_pairs} com uma similaridade de {max_similarity:.2%}\nTempo total de execução: {end - tempo_inicio} segundos"""

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
    print(processa(sequences_str))