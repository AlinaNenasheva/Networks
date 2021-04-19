import socket

class ServerAdress:

    def __init__(self, host='localhost', port=8000):
       self.host = host
       self.port = port
     
class ClientSocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
          

    def connect(self, server_adress):
        self.sock.connect((server_adress.host, server_adress.port)) 


    def send(self, http_request):
        self.sock.send(http_request.encode())
    

    def receive(self):
        response = ''
        while True:
            recv = self.sock.recv(1024).decode()
            if not recv:
                break
            response += recv 
        return response

    
    def close(self):
        self.sock.close()


class ClientRequestCustomHeader:

    def __init__(self, host='localhost', accept='text/html', content_length=212, accept_language='en-US'):
        self.host = host
        self.accept = accept
        self.content_length = content_length
        self.accept_language = accept_language

def main():
    server_address = ServerAdress()
    client_socket = ClientSocket()
    client_socket.connect(server_address)
    client_socket.send('GET / HTTP/1.0\r\nHost: localhost\r\n\r\n')
    print(client_socket.receive())
    client_socket.close()



if __name__ == "__main__":
    main()
    

