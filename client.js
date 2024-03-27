const net = require("net");
const fs = require("fs");

const serverAddress = "/tmp/rpc_socket";

const client = new net.Socket();

function readJSONFile(filePath) {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, "utf8", (err, data) => {
            if (err) {
                reject(err);
            } else {
                resolve(data);
            }
        });
    });
}

(async function main() {
    try {
        const jsonFilePath = "/Users/maimukohagura/dev/recursion/クライアントサーバモデル/Remote-Procedure-Call/test.json";
        const jsonData = await readJSONFile(jsonFilePath);

        client.connect(serverAddress, () => {
            console.log('Connected to server');
            client.write(jsonData);
        });

        client.on('data', (data) => {
            const response = JSON.parse(data);
            console.log(response);
            client.end();
        });

        client.on('close', () => {
            console.log('Connection closed');
        });

        client.on('error', (error) => {
            console.error('Error:', error);
        });
    } catch (error) {
        console.error('Error:', error);
    }
})();
