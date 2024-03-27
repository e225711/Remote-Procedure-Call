import socket
import os
import math
import json

class Function:
    def methods(method, params):
        if method == "floor":
            return Function.floor(*params)
        elif method == "nroot":
            return Function.nroot(*params)
        elif method == "reverse":
            return Function.reverse(*params)
        elif method == "validAnagram":
            return Function.validAnagram(*params)
        elif method == "sort":
            return Function.sort(*params)

    def floor(x):
        return math.floor(x)

    def nroot(n,x):
        return math.floor(x**(1/n))

    def reverse(s):
        return s[::-1]

    def validAnagram(str1,str2):
        return sorted(str1) == sorted(str2)

    def sort(strArr):
        return sorted(strArr)

class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        self.server_address = "/tmp/rpc_socket"

    def connect(self):
        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass
        print("Starting up on {}".format(self.server_address))
        self.sock.bind(self.server_address)
        self.sock.listen(1)

    def recv_data(self):
        connection,client_address = self.sock.accept()
        recv_data = connection.recv(1024)
        recv_data_dict = json.loads(recv_data.decode("utf-8"))
        method = recv_data_dict["method"]
        params = recv_data_dict["params"]
        id = recv_data_dict["id"]
        result = Function.methods(method,params)
        response = {"result":result,"result_type":type(result).__name__,"id":id}
        response = json.dumps(response)
        # connection.sendall(response.encode("utf-8"))

        if recv_data:
            connection.sendall(response.encode("utf-8"))
        else:
            print("No data from",client_address)

    def start(self):
        self.connect()
        try:
            while True:
                self.recv_data()
        finally:
            self.sock.close()

server = Server()
server.start()
