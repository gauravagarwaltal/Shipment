import React from "react";
import { FetchAccount } from "../components/MetaMaskFetch";
import '../components/Form.css'
import STATE_TYPE from "../RequestType";
import { FetchRequests, DeleteRequest } from "./GetSetData";
import { FetchOtherParty, IsValidSignature } from "../contract/contract_transaction";

async function onDeleteClick(index) {
    const sender = await FetchAccount()
    let response = await DeleteRequest(sender, STATE_TYPE.Response, index)
    console.log(response)
}

async function onShowLastState(request) {
    let state = JSON.parse(request)
    let channel_id = Number.parseInt(state[0])
    const sender = await FetchAccount()
    console.log(sender + channel_id + "laststate")
    let key = sender + channel_id + "laststate"
    alert((localStorage.getItem(key)) || "No Signed State Defined")
}

async function onAcceptClick(request, index) {
    // console.log(request)
    // TODO: split content here and set value to storage and also send back status to other the party
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
        console.log(sender + channel_id + "laststate")
        let key = sender + channel_id + "laststate"
        localStorage.setItem(key, request);
        alert("valid signature")
    }
    else {
        alert("invalid signature")
    }
}

class PendingResponses extends React.Component {
    state = {
        pendingResponse: JSON.parse(localStorage.getItem("PendingResponse") || "[]"),
    }

    onChange = async (event) => this.setState({ 'lastState': event.target.value });

    handlePendingState = async (event) => {
        event.preventDefault();
        let sender = await FetchAccount()
        let response = await FetchRequests(sender, STATE_TYPE.Response)
        console.log(response)
        localStorage.setItem('PendingResponse', JSON.stringify(response));
    }

    render() {
        return (
            <div>
                <h2>New State Response</h2>
                <div>
                    <button onClick={this.handlePendingState} className="btn btn-primary">Refresh Pending Response</button>
                    {

                        console.log(this.state.pendingResponse)
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
                                Object.keys(this.state.pendingResponse).map(request => {
                                    return (
                                        <tr key={request}>
                                            <td>
                                                <button
                                                    className="btn btn-outline-danger"
                                                    onClick={() => onDeleteClick(request)}
                                                >
                                                    Delete Request
                                            </button>
                                            </td>
                                            <td>
                                                <button
                                                    className="btn btn-outline-danger"
                                                    onClick={() => onAcceptClick(this.state.pendingResponse[request], request)}
                                                >
                                                    Accept Request
                                            </button>
                                            </td>
                                            <td><span>{this.state.pendingResponse[request]}</span></td>
                                            <td>
                                                <button className="btn btn-outline-danger" onClick={() => onShowLastState(this.state.pendingResponse[request])} >
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

            </div >
        );
    }
};

export default PendingResponses;
