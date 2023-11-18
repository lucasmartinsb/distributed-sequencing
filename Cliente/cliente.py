import xmlrpc.client
import os

def menu():
    modo_paralelizacao = input(
        """Selecione o método de processamento:
    0. Sequencial/Serial (não paralelo)
    1. MPI
    2. Multithreading
    3. Multiprocessing 
    """)
    if modo_paralelizacao not in ("0","1","2","3"):
        print("Opção inválida!")
        menu()
    else:
        threads = None
        relacao_paralelizacao = {
            0:'sequencial',
            1:'mpi',
            2:'multithreading',
            3:'multiprocessing'
        }
        modo_paralelizacao = int(modo_paralelizacao)
        if modo_paralelizacao > 0:
            threads = input("Qual a quantidade de threads/processos a serem usados? (1-...)\n\t")
            if threads.isnumeric() == False or int(threads) < 1:
                print("Opção inválida!")
                menu()
    return relacao_paralelizacao[modo_paralelizacao], threads

def chama_processamento(data, modo_paralelizacao, threads):
    # Criando o proxy para acessar o servidor RPC
    proxy = xmlrpc.client.ServerProxy("http://localhost:4200")
    if threads is None:
        resposta = proxy.processamento(data, modo_paralelizacao)
    else:
        resposta = proxy.processamento(data, modo_paralelizacao, threads)
    return xmlrpc.client.dumps((resposta,))

if __name__ == '__main__':
    with open("input.csv") as f:
        data = f.read()
    modo_paralelizacao, threads = menu()
    resultado = chama_processamento(data=data, modo_paralelizacao=modo_paralelizacao, threads=threads)
    print(resultado)