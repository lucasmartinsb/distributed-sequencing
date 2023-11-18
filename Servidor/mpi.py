from mpi4py import MPI
import time
import sys
from calcula_similaridade import calcula_similaridade

def processa(sequencias_list : list[str]):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    tempo_inicio = time.time()

    # Distribuir o trabalho entre os processos
    tamanho_processo = len(sequencias_list) // size
    indice_inicio = rank * tamanho_processo
    indice_final = indice_inicio + tamanho_processo if rank < size - 1 else len(sequencias_list)

    pares_mais_similares_local, similaridade_local = acha_pares_similares(sequencias=sequencias_list, indice_inicio=indice_inicio, indice_final=indice_final)

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


        tempo_fim = time.time()

        return {
            'Pares' : pares_mais_similares_maximo,
            'Similaridade' : f"{similaridade_maxima:.2%}",
            'Tempo' : tempo_fim - tempo_inicio
        }
    else:
        return ""
    
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