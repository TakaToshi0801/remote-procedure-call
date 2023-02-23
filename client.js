const net = require('net');
const socket_path = "./socket_file"

class Client {
  constructor(address) {
    this.socket = net.createConnection(address);
    this.socket.setTimeout(3000);
    this.socket.on("connect", () => {
      console.log("connected");
    });
    this.socket.on("data", () => {
      console.log("Receiving json file...");
    });
    this.socket.on("end", () => {
      console.log("disconnected");
    });
    this.socket.on("timeout", () => {
      console.log("socket timeout");
      this.socket.destroy();
    });
    this.socket.on("error", (err) => {
      console.error(err.message);
    });
  }

  async write(data) {
    try {
      await new Promise((resolve, reject) => {
        this.socket.write(data, (error) => {
          if (error) {
            reject(error);
          } else {
            resolve();
          }
        });
      });
    } catch (error) {
      console.error(`Failed to send data: ${data}`);
      throw error;
    }
  }

  async sendAllData(data, interval) {
    for (let i = 0; i < data.length; i++) {
      try {
        await this.write(JSON.stringify(data[i]));
        console.log(`Sent data: ${JSON.stringify(data[i])}`);
        if (i < data.length - 1) {
          await new Promise((resolve) => setTimeout(resolve, interval));
        }
      } catch (error) {
        console.error(`Failed to send data: ${JSON.stringify(data[i])}`);
        throw error;
      }
    }
    await new Promise((resolve) => this.socket.end(resolve));
  }
}

const client = new Client(socket_path);
client.sendAllData([
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
    "id": 2
  },
  {
    "method": "reverse",
    "params": "takatoshi",
    "param_types": "string",
    "id": 3
  },
  {
    "method": "validAnagram",
    "params": ["takatoshi", "tishokata"],
    "param_types": ["string", "string"],
    "id": 4
  },
  {
    "method": "sort",
    "params": ["soccer", "baseball", "tennis", "golf"],
    "param_types": "string[]",
    "id": 5
  }
])