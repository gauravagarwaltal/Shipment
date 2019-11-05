import React from "react";
// import PropTypes from "prop-types";
// import { Link } from "react-router-dom";
// import { toast } from "react-toastify";
import './UserList.css'
import { FetchRequests, DeleteRequest, SetRequest } from "../redisApi/GetSetData";
import { FetchAccount } from "./MetaMaskFetch";
import { FetchOtherParty, IsValidSignature } from "../contract/contract_transaction";
import STATE_TYPE from "../RequestType";
import GenerateSignatures from "../contract/CreateSignature";


async function onDeleteClick(index) {
    const sender = await FetchAccount()
    let response = await DeleteRequest(sender, STATE_TYPE.Request, index)
    console.log(response)
}

async function onShowLastState(request) {
    let state = JSON.parse(request)
    let channel_id = Number.parseInt(state[0])
    const sender = await FetchAccount()
    let key = sender + channel_id + "laststate"
    alert(JSON.parse(localStorage.getItem(key)) || "No Signed State Defined")
}

async function onAcceptClick(request, index) {
    let state = JSON.parse(request)
    let channel_id = Number.parseInt(state[0])
    let count = Number.parseInt(state[1])
    let Alice_Cash = Number.parseInt(state[2])
    let Bob_Cash = Number.parseInt(state[3])
    let signature = state[4]

    console.log(channel_id, count, Alice_Cash, Bob_Cash, signature)

    const sender = await FetchAccount()
    const TheOtherParty = await FetchOtherParty(channel_id, sender)
    let checkSig = await IsValidSignature(TheOtherParty, count, Alice_Cash, Bob_Cash, signature)

    if (checkSig === true) {
        signature = await GenerateSignatures(count, Alice_Cash, Bob_Cash)
        let key = sender + channel_id + "laststate"
        localStorage.setItem(key, JSON.stringify(request));
        let lastState = [
            channel_id, count, Alice_Cash, Bob_Cash, signature
        ]
        let response = await SetRequest(TheOtherParty, STATE_TYPE.Response, JSON.stringify(lastState))
        console.log("hello ", response)
        alert("valid signature")
    }
    else {
        alert("invalid signature")
    }
}


class PendingRequests extends React.Component {
    state = {
        pendingStates: JSON.parse(localStorage.getItem("pendingState") || "[]"),
    };
    handlePendingState = async (event) => {
        event.preventDefault();
        let sender = await FetchAccount()
        // console.log(sender)
        let response = await FetchRequests(sender, STATE_TYPE.Request)
        console.log(response)
        localStorage.setItem('pendingState', JSON.stringify(response));
    }


    render() {
        return (
            <div>
                <h2>New State Requests</h2>
                <div>
                    <button onClick={this.handlePendingState} className="btn btn-primary">Refresh Pending States</button>
                    {

                        console.log(this.state.pendingStates)
                    }
                    <table id="table" className="table">
                        <thead>
                            <tr>
                                <th>Decline State</th>
                                <th>Accept State</th>
                                <th>State Details</th>
                                <th>Last Signed State</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                Object.keys(this.state.pendingStates).map(request => {
                                    return (
                                        <tr key={request}>
                                            <td>
                                                <button className="btn btn-outline-danger" onClick={() => onDeleteClick(request)} >
                                                    Delete Request
                                                </button>
                                            </td>
                                            <td>
                                                <button className="btn btn-outline-danger" onClick={() => onAcceptClick(this.state.pendingStates[request], request)} >
                                                    Accept Request
                                                </button>
                                            </td>
                                            <td><span>{this.state.pendingStates[request]}</span></td>
                                            <td>
                                                <button className="btn btn-outline-danger" onClick={() => onShowLastState(this.state.pendingStates[request])} >
                                                    Show Last Signed State
                                                </button>
                                            </td>
                                        </tr>
                                    )
                                }
                                )
                            }
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }
};
export default PendingRequests;
