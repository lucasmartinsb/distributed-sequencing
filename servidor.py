from Bio.Seq import Seq
import pandas as pd
import xmlrpc.server
from io import StringIO
import subprocess
import os

def cria_arquivo_temporario(data_str : str):
    data = StringIO(data_str)
    df = pd.read_csv(data, sep="\t")
    sequences_list = df['intergenicregion_sequence'].unique()
    with open('temp_input', 'w') as file:
        for sequence in sequences_list:
            file.write(f"{sequence}\n")

def processamento_sequencial():
    result = subprocess.run("python3 ./sequencial.py ./temp_input", shell=True, stdout=subprocess.PIPE, text=True)
    os.remove('temp_input')
    return result.stdout

def process_mpi(nucleos : int):
    result = subprocess.run(f"mpiexec -n {nucleos} python3 ./mpi.py ./temp_input", shell=True, stdout=subprocess.PIPE, text=True)
    os.remove('temp_input')
    return result.stdout

def processamento(data_str : str, paralelizacao : str, nucleos : str = None):
    print("Um cliente me chamou!")
    cria_arquivo_temporario(data_str=data_str)
    
    if paralelizacao == 'mpi':
        if nucleos != None:
            return process_mpi(nucleos=int(nucleos)).strip()
        else:
            return "Faltou a quantidade de nucleos amigao"
    elif paralelizacao == 'sequencial':
        return processamento_sequencial().strip()

if __name__ == '__main__':
    #Cria o server
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8001))

    #Registra a funcao
    server.register_function(processamento, "processamento")
    print("Iniciando server...")

    # Mantem em execução
    server.serve_forever() 
    