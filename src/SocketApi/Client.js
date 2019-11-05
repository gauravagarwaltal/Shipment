import React from 'react'
// import { toast } from "react-toastify";
// import {
//     SocketProvider,
//     socketConnect,
// } from 'socket.io-react';

// import { SocketProvider } from 'socket.io-react';
// import io from 'socket.io-client';
// import RenderSubscribedDetails from './RenderSubscribedDetails';
import { IsValidSignature } from '../contract/contract_transaction';
import { FetchAccount } from '../components/MetaMaskFetch';
import GenerateSignatures from '../contract/CreateSignature';
import Socket from "./Socket";

function onDeleteClick(response_array, value) {
    console.log(response_array, value)
    console.log("I'm Happy One")
    console.log("value")
    response_array.splice(value, 1);
    localStorage.setItem('response', JSON.stringify(response_array));
    console.log(response_array.length)
}

async function onAcceptClick(request) {
    console.log(request)
    let ReqObject = JSON.parse(request)
    console.log(ReqObject.channel_id, ReqObject.count, ReqObject.Alice_Cash, ReqObject.Bob_Cash, ReqObject.signature)
    const sender = await FetchAccount()
    const flag = await IsValidSignature(sender, ReqObject.count, ReqObject.Alice_Cash, ReqObject.Bob_Cash, ReqObject.signature)
    console.log(flag)
    let result = await GenerateSignatures(ReqObject.count, ReqObject.Alice_Cash, ReqObject.Bob_Cash)
    console.log(result)
    ReqObject.signature = result.alice
    Socket.emit('publishToChannel', 'newChannel', JSON.stringify(ReqObject));
    console.log("all Done")
}


class ClientClass extends React.Component {
    constructor() {
        super();
        this.state = {
            userId: localStorage.getItem("userId") || '',
            response: JSON.parse(localStorage.getItem("response") || "[]"),
        };
    }

    componentDidMount() {
        console.log(this.state.userId)
        if (this.state.userId !== '') {
            //Very simply connect to the socket
            // this.state.socket.open();
            //Listen for data on the "outgoing data" namespace and supply a callback for what to do when we get one. In this case, we set a state variable
            Socket.on("notification", (channel, message) => {
                console.log("Hello ", message)
                this.state.response.push(message)
                localStorage.setItem('response', JSON.stringify(this.state.response));
            });
            Socket.on('connected', () => {
                var msg = "You are now connected for push notifications";
                console.log(msg);
                // let newValue = JSON.parse(localStorage.getItem("response") || "[]")
                // let value = []
                // // newValue.push(msg)
                // localStorage.setItem('response', JSON.stringify(value));
                // this.setState({ response: newValue })
                // Send the user ID
                Socket.emit('closeChannel', this.state.userId);
                Socket.emit('join', this.state.userId);
            });
        }
    }

    componentWillUnmount() {
        Socket.emit('closeChannel', this.state.userId);
        Socket.close();
    }

    onUserIdChange = async (event) => {
        event.preventDefault();
        this.setState({ userId: event.target.value })
        localStorage.setItem('userId', event.target.value);
    }

    onDeleteClick = async (event) => {
        console.log("value")
        for (var i = 0; i < this.state.response.length; i++) {
            if (this.state.response[i] === event) {
                this.state.response.splice(i, 1);
            }
        }
        localStorage.setItem('response', JSON.stringify(this.state.response));
        console.log("sss")
    }

    render() {
        return (
            <div style={{ textAlign: "center" }}>
                <script src="/socket.io/socket.io.js"></script>
                <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

                <form id="idForm" onSubmit={this.state.componentDidMount} action="">
                    User ID: <input
                        id="userId"
                        type="text"
                        onChange={this.onUserIdChange}
                        name="userId"
                        className="form-control"
                        value={this.state.userId}
                    /><br />
                    <input id="formButton" type="submit" value="Submit" />
                </form>
                <h2>Messages from Subscribed channel ->'{this.state.userId}':</h2>
                <table id="table" className="table">
                    <thead>
                        <tr>
                            <th>Decline State</th>
                            <th>Accept State</th>
                            <th>State Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            Object.keys(this.state.response).map(request => {
                                return (
                                    <tr key={request}>
                                        <td>
                                            <button
                                                className="btn btn-outline-danger"
                                                onClick={() => onDeleteClick(this.state.response, request)}
                                            >
                                                Delete Request
                                            </button>
                                        </td>
                                        <td>
                                            <button
                                                className="btn btn-outline-danger"
                                                onClick={() => onAcceptClick(this.state.response[request])}
                                            >
                                                Accept Request
                                            </button>
                                        </td>
                                        {/* {this.state.response[request].map(user => {
                                            return (
                                                <td>{user}</td>
                                            );
                                        })} */}
                                        <td><span>{this.state.response[request]}</span></td>
                                        {/* <td>{JSON.parse(this.state.response[request])}</td> */}
                                        {/* <td>{this.state.response[request].count}</td> */}
                                        {/* <td>{this.state.response[request]['count']}</td> */}
                                        {/* <td>{this.state.response[request].count}</td> */}
                                    </tr>
                                )

                            }
                            )
                        }
                    </tbody>
                </table>
                {/* <RenderSubscribedDetails details={this.state.response} handleDeleteClick={this.state.onDeleteClick} /> */}
            </div>
        )
    }
}

export default ClientClass;