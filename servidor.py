from Bio.Seq import Seq
import pandas as pd
import xmlrpc.server
from io import StringIO
import subprocess
import os

def process(data_str : str):
    print("Um cliente me chamou!")

    data = StringIO(data_str)
    df = pd.read_csv(data, sep="\t")
    sequences_list = df['intergenicregion_sequence'].unique()
    with open('temp_input', 'w') as file:
        for sequence in sequences_list:
            file.write(f"{sequence}\n")
    result = subprocess.run("python3 ./sequencial.py ./temp_input", shell=True, stdout=subprocess.PIPE, text=True)
    return result.stdout

def process_mpi(data_str : str):
    print("Um cliente me chamou!")

    data = StringIO(data_str)
    df = pd.read_csv(data, sep="\t")
    sequences_list = df['intergenicregion_sequence'].unique()
    with open('temp_input', 'w') as file:
        for sequence in sequences_list:
            file.write(f"{sequence}\n")
    result = subprocess.run("mpiexec -n 4 python3 ./mpi.py ./temp_input", shell=True, stdout=subprocess.PIPE, text=True)
    os.remove('temp_input')
    return result.stdout

if __name__ == '__main__':
    #Cria o server
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8001))

    #Registra a funcao
    server.register_function(process, "processar")
    server.register_function(process_mpi, "processar_mpi")
    print("Iniciando server...")

    # Mantem em execução
    server.serve_forever() 
    