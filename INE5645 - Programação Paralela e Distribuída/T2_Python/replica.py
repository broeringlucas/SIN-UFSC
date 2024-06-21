import socket 
import threading
import json

class Replica: 
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.data = {}

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Replica iniciada em {self.host}:{self.port}")

        while True:
            balanceador_de_carga_socket, address = self.socket.accept()
            threading.Thread(target=self.handle_client, args=(balanceador_de_carga_socket, address)).start()
    
    def handle_client(self, balanceador_de_carga_socket, address):
        data = balanceador_de_carga_socket.recv(1024).decode('utf-8')
        request = json.loads(data)

        print(f"Received request from {address}: {data}") 

        if request['type'] == 'write':
            key = request['key']
            value = request['value']
            self.data[key] = value
            print(f"Stored key-value pair: {key} -> {value}")

        elif request['type'] == 'read':
            key = request['key']
            value = self.data.get(key, None)
            response = json.dumps({'value': value})

            client_address = request['client_address']
            self.send_response_to_client(client_address, response)
        
        print(f"Data: {self.data} Replica {self.host}:{self.port}")

        balanceador_de_carga_socket.close()


    def send_response_to_client(self, client_address, response):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((client_address['host'], client_address['port']))
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()
        print(f"Sent response to client: {response}")

def main():
    with open("INE5645 - Programação Paralela e Distribuída/T2_Python/replica_config.json") as f:
        config = json.load(f)

    for replica_conf in config:
        replica = Replica(replica_conf['host'], replica_conf['port'])
        threading.Thread(target=replica.start).start()

main()