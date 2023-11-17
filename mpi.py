import warnings
warnings.filterwarnings("ignore")
from Bio import pairwise2
from Bio.Seq import Seq
from mpi4py import MPI
import time
import sys

def calculate_similarity(seq1, seq2):
    alignments = pairwise2.align.globalxx(seq1, seq2, one_alignment_only=True)
    score = alignments[0].score
    similarity = score / max(len(seq1), len(seq2))
    return similarity

def find_most_similar_pairs(sequences, start_index, end_index):
    num_sequences = len(sequences)
    most_similar_pairs = []
    max_similarity = 0

    for i in range(start_index, end_index):
        for j in range(i + 1, num_sequences):
            similarity = calculate_similarity(sequences[i], sequences[j])
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_pairs = [(i, j)]
            elif similarity == max_similarity:
                most_similar_pairs.append((i, j))

    return most_similar_pairs, max_similarity

def process(sequences_str : list[str]):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    start = time.time()

    sequences = []
    for sequence in sequences_str:
        sequences.append(Seq(sequence))

    # Distribuir o trabalho entre os processos
    chunk_size = len(sequences) // size
    start_index = rank * chunk_size
    end_index = start_index + chunk_size if rank < size - 1 else len(sequences)

    local_most_similar_pairs, local_max_similarity = find_most_similar_pairs(sequences, start_index, end_index)

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
        return f"""Sequências mais similares são {max_similarity_pairs} com uma similaridade de {max_similarity:.2%}\nTempo total de execução: {end - start} segundos"""

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
    print(process(sequences_str))