import socket 
import json 
import threading
import time
import random

class Cliente: 
    def __init__(self, config, host, port):
        self.id = config['id']
        self.host = host
        self.port = port
        self.requests = config['requests']

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        print(f"Cliente {self.id} iniciado")

        for request in self.requests:
            if request['type'] == 'read':
                response_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                response_socket.bind(("localhost", 0))
                response_socket.listen(1)
                client_host, client_port = response_socket.getsockname()
                request['client_address'] = {'host': client_host, 'port': client_port}
                self.send_request(request)

                response_client_socket, _ = response_socket.accept()
                response = response_client_socket.recv(1024).decode('utf-8')
                response_data = json.loads(response)
                if response_data['value'] == None: 
                    response_data = "Não há valor associado à chave"

                print(f"Cliente {self.id} recebeu resposta da replica: {response_data}")
                response_client_socket.close()
                response_socket.close()

            else:
                self.send_request(request)
                
            time.sleep(random.uniform(1, 2))

        self.socket.close()
        print(f"Cliente {self.id} terminou")
    
    def send_request(self, request):
        self.socket.sendall(json.dumps(request).encode('utf-8'))
        print(f"Cliente {self.id} enviou requisição: {request.get('type'), request.get('key', None), request.get('value', None)}")
    

def main():
    with open("INE5645 - Programação Paralela e Distribuída/T2_Python/cliente_config.json") as f:
        config = json.load(f)

    host = config['balanceador_de_carga']['host']
    port = config['balanceador_de_carga']['port']

    for i in range (len(config['clientes'])):
        client = Cliente(config['clientes'][i], host, port)
        threading.Thread(target=client.start).start()


main()