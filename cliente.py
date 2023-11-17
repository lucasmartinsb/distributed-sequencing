import xmlrpc.client

# Criando o proxy para acessar o servidor RPC
proxy = xmlrpc.client.ServerProxy("http://localhost:8001")

with open("input.csv") as f:
    data = f.read()

resposta = proxy.processar_mpi(data)

print(xmlrpc.client.dumps((resposta,)))