import React, { Component } from 'react';

class Main extends Component {
    constructor(props) {
        super(props);

        this.state = {
            ws: null
        };
    }

    // single websocket instance for the own application and constantly trying to reconnect.

    componentDidMount() {
        this.connect();
    }

    timeout = 250; // Initial timeout duration as a class variable

    /**
     * @function connect
     * This function establishes the connect with the websocket and also ensures constant reconnection if connection closes
     */
    connect = () => {
        var ws = new WebSocket("ws://localhost:5002/");
        let that = this; // cache the this
        var connectInterval;

        // websocket onopen event listener
        ws.onopen = () => {
            console.log("connected websocket main component");

            this.setState({ ws: ws });

            that.timeout = 250; // reset timer to 250 on open of websocket connection 
            clearTimeout(connectInterval); // clear Interval on on open of websocket connection
        };

        // websocket onclose event listener
        ws.onclose = e => {
            console.log(
                `Socket is closed. Reconnect will be attempted in ${Math.min(
                    10000 / 1000,
                    (that.timeout + that.timeout) / 1000
                )} second.`,
                e.reason
            );

            that.timeout = that.timeout + that.timeout; //increment retry interval
            connectInterval = setTimeout(this.check, Math.min(10000, that.timeout)); //call check function after timeout
        };

        // websocket onerror event listener
        ws.onerror = err => {
            console.error(
                "Socket encountered error: ",
                err.message,
                "Closing socket"
            );

            ws.close();
        };
    };

    /**
     * utilited by the @function connect to check if the connection is close, if so attempts to reconnect
     */
    check = () => {
        const { ws } = this.state;
        if (!ws || ws.readyState === WebSocket.CLOSED) this.connect(); //check if websocket instance is closed, if so call `connect` function.
    };

    render() {
        return <div >websocket={this.state.ws} </div>;
    }
}

export default Main;
// import { WebSocket } from "ws";
// // var WebSocket = require('ws')
// import { redis_connection } from "redis-connection";
// function testJSON() {
//     var jsonSocket = new WebSocket("ws://127.0.0.1:6379/.json");
//     jsonSocket.onopen = function () {

//         console.log("JSON socket connected!");
//         jsonSocket.send(JSON.stringify(["SET", "hello", "world"]));
//         jsonSocket.send(JSON.stringify(["GET", "hello"]));
//     };
//     jsonSocket.onmessage = function (messageEvent) {
//         console.log("JSON received:", messageEvent.data);
//     };
// }

// function RedisConnection() {
//     let redisClient = redis_connection; // require & connect
//     redisClient.set('hello', 'world');
//     redisClient.get('hello', function (err, reply) {
//         console.log('hello', reply.toString()); // hello world
//         redisClient.end(true); // this will "flush" any outstanding requests to redis
//     });
// }
// export default RedisConnection;