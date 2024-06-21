import socket 
import threading
import json 

class BalanceadorDeCarga: 
    def __init__(self, config):
        self.replicas = [(replica['host'], replica['port']) for replica in config['replicas']]
        self.host = config['host']
        self.port = config['port']
        self.next = 0 
        self.lock = threading.Lock()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Balanceador de carga iniciado em {self.host}:{self.port}")

        while True:
            client_socket, address = self.socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, address)).start()
    
    def handle_client(self, client_socket, address):
        data = client_socket.recv(1024).decode('utf-8')
        request = json.loads(data)

        print(f"Received request from {address}: {data}") 

        print(request)

        if request['type'] == 'write': 
            for replica in self.replicas: 
                print(f"Sending request to {replica}")
                self.send_to_replica(replica, request)
            client_socket.sendall(b"OK")
            print("Request completed")

        elif request['type'] == 'read':
            with self.lock:
                replica = self.replicas[self.next]	
                print(replica)
                self.next = (self.next + 1) % len(self.replicas)
            print(f"Sending request to {replica}")
            request['client_address'] = {'host': address[0], 'port': client_socket.getsockname()[1]}
            print(request)

            self.send_to_replica(replica, request)

        client_socket.close()
    
    def send_to_replica(self, replica, request):
        replica_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        replica_socket.connect(replica)
        replica_socket.sendall(json.dumps(request).encode('utf-8'))
        replica_socket.close()
    
def main():
    with open("INE5645 - Programação Paralela e Distribuída/T2_Python/balanceador_de_cargas_config.json") as f:
        config = json.load(f)

    balanceador = BalanceadorDeCarga(config)
    balanceador.start()

main()