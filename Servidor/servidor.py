from Bio.Seq import Seq
import pandas as pd
import xmlrpc.server
from io import StringIO
import subprocess
import os
from datetime import datetime
import json

def cria_arquivo_temporario(data_str : str):
    data = StringIO(data_str)
    df = pd.read_csv(data, sep="\t")
    sequences_list = df['intergenicregion_sequence'].unique()
    with open('temp_input', 'w') as file:
        for sequence in sequences_list:
            file.write(f"{sequence}\n")

def processamento_normal():
    result = subprocess.run("python3 ./normal.py ./temp_input", shell=True, stdout=subprocess.PIPE, text=True)
    os.remove('temp_input')
    return result.stdout

def processamento_mpi(threads : int):
    result = subprocess.run(f"mpiexec -n {threads} python3 ./mpi.py ./temp_input", shell=True, stdout=subprocess.PIPE, text=True)
    os.remove('temp_input')
    return result.stdout

def processamento_multiprocessing(threads : int):
    result = subprocess.run(f"python3 ./multiprocessing.py ./temp_input {threads}", shell=True, stdout=subprocess.PIPE, text=True)
    os.remove('temp_input')
    return result.stdout

def processamento_multithreading(threads : int):
    result = subprocess.run(f"python3 ./multithreading.py ./temp_input {threads}", shell=True, stdout=subprocess.PIPE, text=True)
    os.remove('temp_input')
    return result.stdout

def processamento(data_str : str, paralelizacao : str, threads : str = None):
    print(f"""\n
    {datetime.now()} - Um cliente me chamou!
        Modo de paralelização: {paralelizacao}
        Threads: {threads}""")
    cria_arquivo_temporario(data_str=data_str)

    if paralelizacao == 'mpi':
        resultado = processamento_mpi(threads=int(threads)).strip()
    elif paralelizacao == 'multiprocessing':
        resultado = processamento_multiprocessing(threads=int(threads)).strip()
    elif paralelizacao == 'multithreading':
        resultado = processamento_multithreading(threads=int(threads)).strip()
    elif paralelizacao == 'sequencial':
        resultado = processamento_normal().strip()

    print(f"    {datetime.now()} - Finalizou\n")
    return resultado

if __name__ == '__main__':
    #Cria o server
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 4200))

    #Registra a funcao
    server.register_function(processamento, "processamento")
    print("Iniciando server...")

    # Mantem em execução
    server.serve_forever() 
    