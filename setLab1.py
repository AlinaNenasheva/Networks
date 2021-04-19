import socket
import argparse
from string import Template
import http-parser

parser_arg = argparse.AgrumentParser()
http_parser = HttpParser()

def init_parse_args():
    parser_arg.add_argument('h', 'host', type=str, help='this is port')
    parser_arg.add_argument('a', 'accept', help='accepted type of content')
    parser_arg.add_argument('cl', 'content_length', help='the length of content')
    parser_arg.add_argument('al', 'accept_language', help='the language of content')
    args = parser_arg.parse_args()
    return args
   

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
            data = self.sock.recv(1024).decode()
            if not data:
                break
            response += data
        return response


    def ger_error_description(data):
        
    
    
    def close(self):
        self.sock.close()


class HTTPRequest:
    
    def __init__(method, path, header, body):
        self.method = method
        self.path = path
        self.header = header
        self.body = body


    def create_request(self):
        request = "$self.method $self.path HTTP/1.1\r\n"
        request += "$self.header\r\n"
        request += "$self.body\r\n"
        return request


class ClientRequestCustomHeader:

    def __init__(self, host='localhost', accept='text/html', content_length=212, accept_language='en-US'):
        self.host = host
        self.accept = accept
        self.content_length = content_length
        self.accept_language = accept_language
    
    
    def create_header(self):
        header = ""
        header += "Host: $self.host\r\n"
        header += "Accept: $self.accept\r\n"
        header += "Accept-Language: $self.accept_language\r\n"
        header += "Content-Length: $self.content_length\r\n"
        return header
       
       
class HTTPBody:
      
    @classmethod
    def get_from_commandline(cls, args):
        return cls(args.body)
        
    @classmethod
    def load_from_file(cls, path):
        return(open(path, 'r').read())
        

def main():
    server_address = ServerAdress()
    client_socket = ClientSocket()
    client_socket.connect(server_address)
    client_socket.send('GET / HTTP/1.0\r\nHost: localhost\r\n\r\n')
    print(client_socket.receive())
    client_socket.close()



if __name__ == "__main__":
    main()
    

