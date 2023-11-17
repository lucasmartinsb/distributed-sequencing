import warnings
warnings.filterwarnings("ignore")
from Bio.Seq import Seq
from Bio import pairwise2
import time
import sys

def calculate_similarity(seq1, seq2):
    alignments = pairwise2.align.globalxx(seq1, seq2, one_alignment_only=True)
    score = alignments[0].score
    similarity = score / max(len(seq1), len(seq2))
    return similarity

def find_most_similar_pairs(sequences):
    num_sequences = len(sequences)
    most_similar_pairs = []
    max_similarity = 0

    for i in range(num_sequences):
        for j in range(i + 1, num_sequences):
            similarity = calculate_similarity(sequences[i], sequences[j])
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_pairs = [(i, j)]
            elif similarity == max_similarity:
                most_similar_pairs.append((i, j))

    return most_similar_pairs, max_similarity

def process(sequences_str : list[str]):
    start = time.time()
    
    # Encontrar os pares mais similares e a similaridade geral
    most_similar_pairs, overall_similarity = find_most_similar_pairs(sequences_str)
    
    end = time.time()
    
    # Imprimir os resultados
    return (f"Sequências mais similares são {most_similar_pairs} com uma similaridade de {overall_similarity:.2%}.", end - start)

if __name__ == '__main__':
    inFile = sys.argv[1]
    sequences_str = []
    with open(inFile,'r') as inputFile:
        for line in inputFile:
            # Remove espaços em branco e caracteres de nova linha
            sequence = line.strip()
            # Adiciona o item à lista
            sequences_str.append(sequence)
    print(process(sequences_str=sequences_str))