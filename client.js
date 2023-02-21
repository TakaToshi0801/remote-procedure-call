const net = require('net');
const socket_path = "./socket_file"

class Client {
    constructor(address) {
        this.__socket = net.createConnection(address);
        this.__socket.setTimeout(3000);
        this.__socket.on("connect", () => {
            console.log("connected");
        });
        this.__socket.on("data", (data) => {
            console.log("Receiving json file...");
        });
        this.__socket.on("end", () => {
            console.log("disconnected");
        });
        this.__socket.on("timeout", () => {
            console.log("socket timeout");
            this.__socket.destroy();
        })
        this.__socket.on("error", (err) => {
            console.error(err.message);
        });
    }
    write(data) {
        this.__socket.write(data);
    }
}

data = [
    {
        "method": "floor",
        "params": 3.1415,
        "param_types": "double",
        "id": 1
    },
    {
        "method": "nroot",
        "params": [3, 9],
        "param_types": ["int", "int"],
        "id": 1
    },
    {
        "method": "reverse",
        "params": "takatoshi",
        "param_types": "string",
        "id": 1
    },
    {
        "method": "validAnagram",
        "params": ["takatoshi", "tishokata"],
        "param_types": ["string", "string"],
        "id": 1
    },
    {
        "method": "sort",
        "params": ["soccer", "baseball", "tennis", "golf"],
        "param_types": "string[]",
        "id": 1
    }
]

client = new Client(socket_path);
for(let i = 0; i < data.length; i++){
    setTimeout(() => {
        client.write(JSON.stringify(data[i]));
    }, i * 1000);
}