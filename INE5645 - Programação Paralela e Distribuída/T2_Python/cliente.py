import socket
import json
import time
import random

def send_request(client_socket, request):
    client_socket.sendall(json.dumps(request).encode('utf-8'))
    print(f"Sent request: {request}")

def run_client(client_id, requests, load_balancer):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((load_balancer['host'], load_balancer['port']))
    print(f"Client {client_id} started")

    for request in requests:
        if request['type'] == 'read':
            # Open a listening socket for the response
            response_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            response_socket.bind(("localhost", 0))
            response_socket.listen(1)
            client_host, client_port = response_socket.getsockname()
            request['client_port'] = client_port
            send_request(client_socket, request)

            response_client_socket, _ = response_socket.accept()
            response = response_client_socket.recv(1024).decode('utf-8')
            response_data = json.loads(response)
            print(f"Received response from replica: {response_data}")
            response_client_socket.close()
            response_socket.close()
        else:
            send_request(client_socket, request)
        
        time.sleep(random.uniform(1, 2))

    client_socket.close()
    print(f"Client {client_id} finished")

if __name__ == "__main__":
    with open('INE5645 - Programação Paralela e Distribuída/T2_Python/cliente_config.json') as f:
        config = json.load(f)
    
    load_balancer = config['load_balancer']
    clients = config['clients']

    for client in clients:
        client_id = client['id']
        requests = client['requests']
        run_client(client_id, requests, load_balancer)

    print("All clients finished")
