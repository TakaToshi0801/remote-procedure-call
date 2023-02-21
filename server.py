import socket
import json
import os
import math


class Server:
    def __init__(self, socket_path):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket_path = socket_path
    
    def start(self):
        try:
            os.unlink(self.socket_path)
        except FileNotFoundError:
            pass

        print('Starting on up {}'.format(self.socket_path))
        self.sock.bind(self.socket_path)
        self.sock.listen(1)
        self.accepted()
        
    def accepted(self):
        while True:
            connection, address = self.sock.accept()
            try:
                while True:
                    recv_data = connection.recv(1024).decode('utf-8')
                    print('Receive data: {}'.format(recv_data))
                    print("---------------------------")
                    if recv_data:
                        self.respond(connection, recv_data)
                    else:
                        print('No data.')
                        break
            finally:
                print('Closing current connection.')
                connection.close()
        
    def respond(self, connection, recv_data):
        try:
            response = JsonProcessor.process(json.loads(recv_data))
            connection.sendall(response.encode())
        except Exception:
            pass


class JsonProcessor:
    processor = {
        "floor": (lambda x: math.floor(x), "int"),
        "nroot": (lambda params: (params[1] ** (1/params[0])), "double"),
        "reverse": (lambda s: s[::-1], "string"),
        "validAnagram":(lambda params: set(params[0]) == set(params[1]), "string"),
        "sort":(lambda strArr: sorted(strArr), "string[]")
    }

    def process(jsondata):
        try:
            method = jsondata["method"]
            params = jsondata["params"]
            param_types= jsondata["param_types"]
            id = jsondata["id"]

            res_method = JsonProcessor.processor[method][0](params)
            res_type = JsonProcessor.processor[method][1]
            return JsonProcessor.create_json_file(res_method, res_type, id)

        except Exception as e:
            return {"error": e}

    def create_json_file(result, resultType, id):
        path = './output.json'
        dict_obj = {
            "result":result,
            "result_types":resultType,
            "id":id
        }

        ls = None
        with open(path, 'r+') as f:
            ls = f.readlines()
            if ls == []:
                ls.append('[\n')
            if ls[-1] == ']':
                ls[-1] = ','
            ls.insert(len(ls), '{}'.format(json.dumps(dict_obj, indent=4, ensure_ascii=False)))
            ls.insert(len(ls), '\n]')

        with open(path, 'w') as f:
            f.writelines(ls)

def main():
    socket_path = './socket_file'
    server = Server(socket_path)
    server.start()

if __name__ == "__main__":
    main()