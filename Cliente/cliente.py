import xmlrpc.client
import os
import xml.etree.ElementTree as ET
import ast

def xml_to_dict(xml_string):
    root = ET.fromstring(xml_string)
    result = {}
    for child in root:
        if len(child) == 0:
            result[child.tag] = child.text
        else:
            result[child.tag] = xml_to_dict(ET.tostring(child))
    return result

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
    resposta_xml = xml_to_dict(xmlrpc.client.dumps((resposta,)))
    resposta_str = resposta_xml["param"]["value"]["string"]
    resposta_str = resposta_str.replace("\'", "\"")
    resposta_dict = ast.literal_eval(resposta_str)
    return resposta_dict

if __name__ == '__main__':
    with open("input.csv") as f:
        data = f.read()
    modo_paralelizacao, threads = menu()
    resultado = chama_processamento(data=data, modo_paralelizacao=modo_paralelizacao, threads=threads)
    print(f"""
    Pares: {resultado['Pares']}
    Similaridade: {resultado['Similaridade']}
    Tempo: {resultado['Tempo']}
    """)