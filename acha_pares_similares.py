from calcula_similaridade import calcula_similaridade

def acha_pares_similares_sequencial(sequencias):
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


def acha_pares_similares_mpi(sequencias, indice_inicio, indice_final):
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