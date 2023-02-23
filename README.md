# RPC(Remote Procedure Call)

RPCとは、ネットワーク上にある他のコンピュータのプログラムを呼び出し、機能やタスクを実行させるための技術

## 概要

クライアントとサーバが異なるプログラミング言語で書かれていても、クライアントプログラムがサーバ上の機能を呼び出せるようなシステムを構築しました。

UNIXドメインソケットを使って、クライアントからJSON形式のデータを受信し、そのデータに対応する処理を実行するサーバと、クライアントを実装しました。クライアントは、TCP接続でサーバに接続し、JSON形式のデータを送信します。サーバはデータを受信して、それをJSON形式に解析し、適切な処理を呼び出します。処理の結果は、JSON形式の応答としてクライアントに返されます。また、複数のクライアントからの接続を処理するために、スレッドを使用しています。

サーバは、以下の関数をRPCとしてクライアントに提供します。

・floor(double x) : 10 進数 x を最も近い整数に切り捨て、その結果を整数で返す。
・nroot(int n, int x) : 方程式 rn = x における、r の値を計算する。
・reverse(string s) : 文字列 s を入力として受け取り、入力文字列の逆である新しい文字列を返す。
・validAnagram(string str1, string str2) : 2 つの文字列を入力として受け取り，2 つの入力文字列が互いにアナグラムであるかどうかを示すブール値を返す。
・sort(string[] strArr) : 文字列の配列を入力として受け取り、その配列をソートして、ソート後の文字列の配列を返す。

## 実行方法と結果

### サーバ(Python)

```bash
> python3 server.py
Starting on up ./socket_file
Accepted connection
Receive data: {"method":"floor","params":3.1415,"param_types":"double","id":1}
---------------------------
Receive data: {"method":"nroot","params":[3,9],"param_types":["int","int"],"id":2}
---------------------------
Receive data: {"method":"reverse","params":"takatoshi","param_types":"string","id":3}
---------------------------
Receive data: {"method":"validAnagram","params":["takatoshi","tishokata"],"param_types":["string","string"],"id":4}
---------------------------
Receive data: {"method":"sort","params":["soccer","baseball","tennis","golf"],"param_types":"string[]","id":5}
---------------------------
Receive data:
---------------------------
No data.
Closing current connection.
```

### クライアント(JavaScript)

```bash
> node client.js
Connected
Sent data: {"method":"floor","params":3.1415,"param_types":"double","id":1}
Receive data: {"result": 3, "result_types": "int", "id": 1}
Sent data: {"method":"nroot","params":[3,9],"param_types":["int","int"],"id":2}
Receive data: {"result": 2.080083823051904, "result_types": "double", "id": 2}
Sent data: {"method":"reverse","params":"takatoshi","param_types":"string","id":3}
Receive data: {"result": "ihsotakat", "result_types": "string", "id": 3}
Sent data: {"method":"validAnagram","params":["takatoshi","tishokata"],"param_types":["string","string"],"id":4}
Receive data: {"result": true, "result_types": "string", "id": 4}
Sent data: {"method":"sort","params":["soccer","baseball","tennis","golf"],"param_types":"string[]","id":5}
Receive data: {"result": ["baseball", "golf", "soccer", "tennis"], "result_types": "string[]", "id": 5}
Disconnected
```