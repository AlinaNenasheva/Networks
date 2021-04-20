import socket
import argparse
import re

STATUSES = ['200', '404', '301', '500', '501', '401', '402', '403', '201']

parser_arg = argparse.ArgumentParser()

def init_parse_args():
    parser_arg.add_argument('-P', '--path', type=str, help='path for resourse')
    parser_arg.add_argument('--port', type=int, help='port of endpoint')
    parser_arg.add_argument('-M', '--method', type=str, help='method type')
    parser_arg.add_argument('-HT', '--host', type=str, help='host of endpoint')
    parser_arg.add_argument('-A', '--accept', type=str, help='accepted type of content')
    parser_arg.add_argument('-AL', '--accept_language', type=str, help='the language of content')
    parser_arg.add_argument('-H', '--header', action='append', type=str, help='any pair of key : value')
    parser_arg.add_argument('-B', '--body', help='body of the request')
    args = parser_arg.parse_args()
    return args


def parse_body(body):
    return re.sub("[{}]", "", body)


def parse_any_header(headers):
    headers_dict = {header.split(": ")[0] : header.split(": ")[1] for header in headers}
    return headers_dict


def print_status_and_body(response_tuple):
    status_message = ""
    if response_tuple[0] == '404':
        status_message = "You attempt to access broken link."
    if response_tuple[0] == '200':
        status_message = "Successful HTTP request."
    if response_tuple[0] == '301':
        status_message = "Resource moved permanently."
    if response_tuple[0] == '500':
        status_message = "Internal server error."
    if not response_tuple[1]:
        print(f'{response_tuple[0]}. {status_message}')
    else: print(f'{response_tuple[0]}. {status_message} \nBody of response: \n{response_tuple[1]}')


class ServerAdress:

    def __init__(self, headers, host='localhost', port=8000):
        if host:
            self.host = host
        elif "Host" in headers:
            self.host = headers["Host"]
        else:
            self.host = 'localhost'
            
        if not port:
            self.port = 8000
        else:
            self.port = port


class HTTPRequestParser:
    
    def __init__(self, data):
        self.data = data
    
    
    def parse_data(self):
        data_list = self.data.split("\r\n\r\n")
        self.head = data_list[0]
        self.body = None
        if len(data_list) != 1:
            self.body = data_list[1]
        status_code = self.parse_head()
        return (status_code, self.body)
    
    
    def parse_head(self):
        for status in STATUSES:
            if status in self.head:
                return status
                
                
                
     
class ClientSocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        

    def connect(self, server_address):
        self.sock.connect((server_address.host, server_address.port))


    def send(self, http_request):
        self.sock.send(http_request.encode())
    

    def receive(self):
        response = ''
        while True:
            data = self.sock.recv(1024).decode()
            print(data)
            if not data:
                break
            response += data
        print(response)
        return response
    
    
    def close(self):
        self.sock.close()


class HTTPRequest:
    
    def __init__(self, header, body, method, path):
        if not method:
            self.method = 'GET'
        else:
            self.method = method
        if not path:
            self.path = '/'
        else:
            self.path = path
        self.header = header
        self.body = body


    def create_request(self):
        request = f'{self.method} {self.path} HTTP/1.1\r\n'
        request += f'{self.header}\r\n'
        if self.body:
            request += f'{self.body}\r\n'
        return request


class HTTPCustomHeader:

    def __init__(self, any_headers, host, accept, accept_language, body):
            
        if host:
            self.host = host
        elif "Host" in any_headers:
            self.host = any_headers["Host"]
        else:
            self.host = 'localhost'

        if accept:
            self.accept = accept
        elif "Accept" in any_headers:
            self.accept = any_headers["Accept"]
        else:
            self.accept = 'text/html'
            
        if accept_language:
            self.accept_language = accept_language
        elif "Accept-Language" in any_headers:
            self.accept_language = any_headers["Accept-Language"]
        else:
            self.accept_language = 'en-US'
        self.body_length = None
        if body:
            self.body_length = body.body_length
                
    
    def create_header(self):
        header = ""
        header += f'Host: {self.host}\r\n'
        header += f'Accept: {self.accept}\r\n'
        header += f'Accept-Language: {self.accept_language}\r\n'
        if self.body_length:
            header += f'Accept-Language: {self.body_length}\r\n'
        return header
       
       
class HTTPBody:

    @property
    def body_length(self):
        return len(self.body)

    @classmethod
    def get_from_commandline(cls, args):
        item = cls()
        item.body = args.body
        return item
        
    @classmethod
    def load_from_file(cls, path):
        item = cls()
        item.body = open(path, 'r').read()
        return item


def main():
    args = init_parse_args()
    server_address = ServerAdress(parse_any_header(args.header), args.host, args.port)
    client_socket = ClientSocket()
    client_socket.connect(server_address)
    http_body = HTTPBody().load_from_file("body.txt")
    http_header = HTTPCustomHeader(parse_any_header(args.header), args.host, args.accept, args.accept_language, http_body)
#    http_body = HTTPBody().get_from_commandline(args).body
    http_request = HTTPRequest(method=args.method, path=args.path, header=http_header.create_header(), body=http_body.body)
    print(f"REQUEST PRINTED: \n{http_request.create_request()}")
    client_socket.send(http_request.create_request())
    response = client_socket.receive()
#    print(f"RESPONSE PRINTED: \n{response}")
    http_parser = HTTPRequestParser(response)
    print_status_and_body(http_parser.parse_data())
    client_socket.close()



if __name__ == "__main__":
    main()
    
