from Bio.Seq import Seq
from Bio import pairwise2
import pandas as pd
import xmlrpc.server
from io import StringIO
import time

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

def process(data_str : str):
    print("Um cliente me chamou!")
    start = time.time()

    data = StringIO(data_str)
    df = pd.read_csv(data, sep="\t")
    sequences_str = df['intergenicregion_sequence'].unique()
    sequences = []
    for sequence in sequences_str:
        sequences.append(Seq(sequence))
    # Encontrar os pares mais similares e a similaridade geral
    most_similar_pairs, overall_similarity = find_most_similar_pairs(sequences)
    
    end = time.time()
    
    # Imprimir os resultados
    return (f"Sequências mais similares são {most_similar_pairs} com uma similaridade de {overall_similarity:.2%}.", end - start)

if __name__ == '__main__':
    #Cria o server
    print("Iniciando server...")
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8001))

    #Registra a funcao
    server.register_function(process, "processar")

    # Mantem em execução
    server.serve_forever() 