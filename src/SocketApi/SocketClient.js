// const express = require('express');
// const socketIO = require('socket.io');
// const http = require('http')
// const port = process.env.PORT || 3000
// var app = express();
// let server = http.createServer(app)
// var io = socketIO(server);



// // connection with server 
// io.on('connect', function () {
//     console.log('Connected to Server')

// });

// // message listener from server 
// io.on('newMessage', function (message) {
//     console.log(message);
// });

// // emits message from user side 
// io.emit('createMessage', {
//     to: 'john@ds',
//     text: 'what kjkljd'
// });

// // when disconnected from server 
// io.on('disconnect', function () {
//     console.log('Disconnect from server')
// });

const WebSocket = require('ws');

let socket = new WebSocket("ws://localhost:5000");

socket.onopen = function (e) {
    console.log("[open] Connection established");
    console.log("Sending to server");
    socket.send("My name is John");
};

socket.onmessage = function (event) {
    console.log(`[message] Data received from server: ${event.data}`);
};

socket.onclose = function (event) {
    if (event.wasClean) {
        console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        console.log('[close] Connection died');
    }
};

socket.onerror = function (error) {
    console.log(`[error] ${error.message}`);
};