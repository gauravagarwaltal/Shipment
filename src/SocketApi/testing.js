import React from 'react'
import {
    SocketProvider,
    socketConnect,
} from 'socket.io-react';

// import { SocketProvider } from 'socket.io-react';
import io from 'socket.io-client';


const socket = io.connect('http://127.0.0.1:5000');
socket.on('message', msg => console.log(msg));

const SocketReact = async => {

    return (
        <SocketProvider socket={socket}>
            <div>sicjdoifj</div>
        </SocketProvider>
    )
}

export default SocketReact;