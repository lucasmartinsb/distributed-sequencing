from Bio.Seq import Seq
import pandas as pd
import socket
import threading
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

def processamento_sequencial():
    result = subprocess.run("python3 ./sequencial.py ./temp_input", shell=True, stdout=subprocess.PIPE, text=True)
    os.remove('temp_input')
    return result.stdout

def processamento_mpi(threads : int):
    result = subprocess.run(f"mpiexec -f ./cluster.txt -n {threads} python3 ./mpi.py ./temp_input", shell=True, stdout=subprocess.PIPE, text=True)
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
        resultado = processamento_sequencial().strip()

    print(f"    {datetime.now()} - Finalizou\n")
    return resultado

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 4200))
    server.listen(5)
    print("Iniciando server...")

    while True:
        client, addr = server.accept()
        handle_client(client)

def handle_client(client_socket):
    data_parts = []
    
    while True:
        part = client_socket.recv(1024).decode('utf-8')
        if not part:
            break
        data_parts.append(part)

    full_data = ''.join(data_parts)
    data_str, paralelizacao, threads = full_data.split(',')
    print(paralelizacao)
    print(threads)
    
    resposta = processamento(data_str=data_str, paralelizacao=paralelizacao, threads=threads)
    client_socket.send(resposta.encode('utf-8'))
    client_socket.close()

if __name__ == '__main__':
    start_server()
