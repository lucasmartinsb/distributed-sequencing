import warnings
warnings.filterwarnings("ignore")
from Bio import pairwise2

def calcula_similaridade(seq1, seq2):
    alinhamento = pairwise2.align.globalxx(seq1, seq2, one_alignment_only=True)
    score = alinhamento[0].score
    similaridade = score / max(len(seq1), len(seq2))
    return similaridade