import xmlrpc.client

# Criando o proxy para acessar o servidor RPC
proxy = xmlrpc.client.ServerProxy("http://localhost:4200")

with open("input.csv") as f:
    data = f.read()



resposta = proxy.processamento(data, 'mpi', 8)

print(xmlrpc.client.dumps((resposta,)))