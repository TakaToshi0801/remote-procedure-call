import socket
import json
import os
import math
import threading

class Server:
    def __init__(self, socket_path):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket_path = socket_path
    
    def start(self):
        try:
            os.unlink(self.socket_path)
        except FileNotFoundError:
            pass

        print('Starting on up {}'.format(self.socket_path))
        self.socket.bind(self.socket_path)
        self.socket.listen(1)
        while True:
            connection, address = self.socket.accept()
            print("Accepted connection")
            # 新しいスレッドを作成
            client_thread = threading.Thread(target=self.accepted, args=(connection,))
            # スレッドを開始
            client_thread.start()

    def accepted(self, connection):
        try:
            while True:
                # クライアントからデータを受信
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
            # レスポンスをクライアントに送信
            connection.sendall(response.encode())
        except Exception:
            print('Error occurred: {}'.format(str(e)))
            error_response = {"error": str(e)}
            connection.sendall(json.dumps(error_response).encode())

class JsonProcessor:
    # メソッドに対応した処理
    processor = {
        "floor": (lambda x: math.floor(x), "int"),
        "nroot": (lambda params: (params[1] ** (1/params[0])), "double"),
        "reverse": (lambda s: s[::-1], "string"),
        "validAnagram":(lambda params: set(params[0]) == set(params[1]), "string"),
        "sort":(lambda strArr: sorted(strArr), "string[]")
    }

    def process(jsondata):
        try:
            # JSONデータからメソッド名、引数、引数の型、idを取得
            method = jsondata["method"]
            params = jsondata["params"]
            param_types= jsondata["param_types"]
            id = jsondata["id"]

            res_method = JsonProcessor.processor[method][0](params)
            res_type = JsonProcessor.processor[method][1]
            response = {"result": res_method, "result_types": res_type, "id": id}
            # 辞書型を文字列に変換して返す
            return json.dumps(response)

        except Exception as e:
            print('Error occurred: {}'.format(str(e)))
            response = {"error": str(e)}
            # 辞書型を文字列に変換して返す
            return json.dumps(response)

def main():
    socket_path = './socket_file'
    server = Server(socket_path)
    server.start()

if __name__ == "__main__":
    main()