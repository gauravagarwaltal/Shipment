import React from "react";
// import GenerateSignatures from "../contract/CreateSignature";
import { IsValidSignature, FetchOtherParty } from "../contract/contract_transaction";
import { FetchAccount } from "./MetaMaskFetch";
import './Form.css'
import GenerateSignatures from "../contract/CreateSignature";
import { SetRequest } from "../redisApi/GetSetData";
import STATE_TYPE from "../RequestType";
// import { toast } from "react-toastify";
// const axios = require('axios');

function ShowState(props) {
    return (
        <div>
            {console.log(props.state)}
            <table id="table" className="table">
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr key="Channel Id">
                        <td><span>Channel Id</span></td>
                        <td><span>{props.state[0]}</span></td>
                    </tr>
                    <tr key="Transaction Count">
                        <td ><span>Transaction Count</span></td>
                        <td><span>{props.state[1]}</span></td>
                    </tr>
                    <tr key="Alice Cash">
                        <td ><span>Alice Cash</span></td>
                        <td><span>{props.state[2]}</span></td>
                    </tr>
                    <tr key="Bob Cash">
                        <td ><span>Bob Cash</span></td>
                        <td><span>{props.state[3]}</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    )
}

class CreateTransaction extends React.Component {
    state = {
        errors: '',
        error: '',
        channel_id: '',
        channelId: '',
        count: '',
        aliceCash: '',
        bobCash: '',
        lastState: null
    }

    // const [course, setCourse] = useState({
    //     channelId: "",
    //     count: "",
    //     AliceCash: "",
    //     BobCash: "",
    //     Signature: ""
    // });
    // localStorage.setItem(props.channelId + 'lastState', lastState);

    onChange = async (event) => this.setState({ 'lastState': event.target.value });

    handleConfirmChannel = async (event) => {
        event.preventDefault();
        this.setState({ 'errors': "" })
        if (Number.isNaN(parseInt(this.state.channelId, 10))) {
            this.setState({ 'errors': "Enter natural number" })
        }
        else if (Number.isNaN(parseInt(this.state.count, 10))) {
            this.setState({ 'errors': "Enter natural number" })
        }
        else if (Number.isNaN(parseInt(this.state.aliceCash, 10))) {
            this.setState({ 'errors': "Enter Integer amount(in wei unit)" })
        }
        else if (Number.isNaN(parseInt(this.state.bobCash, 10))) {
            this.setState({ 'errors': "Enter Integer amount(in wei unit)" })
        }
        else {
            let sig = await GenerateSignatures(this.state.count, this.state.aliceCash, this.state.bobCash)
            console.log(sig)
            let sender = await FetchAccount()
            console.log(await IsValidSignature(sender, this.state.count, this.state.aliceCash, this.state.bobCash, sig))
            this.setState({
                'lastState': [
                    this.state.channelId, this.state.count, this.state.aliceCash, this.state.bobCash, sig
                ]
            })
            localStorage.setItem(sender + this.state.channelId + 'lastState', JSON.stringify(this.state.lastState));
            let TheOtherParty = await FetchOtherParty(this.state.channelId, sender)
            let response = await SetRequest(TheOtherParty, STATE_TYPE.Request, JSON.stringify(this.state.lastState))
            console.log("hello ", response)
        }
        this.setState({ 'channelId': "" })
        this.setState({ 'count': "" })
        this.setState({ 'aliceCash': "" })
        this.setState({ 'bobCash': "" })


    }

    handleLastChannelState = async (event) => {
        event.preventDefault();
        this.setState({ 'error': "" })
        if (Number.isNaN(parseInt(this.state.channel_id, 10))) {
            this.setState({ 'error': "Enter natural number" })
        }
        else {
            let sender = await FetchAccount()
            this.setState({ 'lastState': JSON.parse(localStorage.getItem(sender + this.state.channel_id + 'lastState')) })
        }
    }

    render() {
        return (
            <div>
                <h2>Channel Details</h2>
                <div>
                    <div>
                        <h3>Fetch Last Signed state </h3>
                        <form id="form" className="mt-2" onSubmit={this.handleLastChannelState}>
                            <div className="form-group">
                                <label htmlFor="channel_id">Channel Id</label>
                                <div className="field">
                                    <input
                                        id="channel_id"
                                        onChange={event => this.setState({ channel_id: event.target.value })}
                                        type="text"
                                        name="channel_id"
                                        className="form-control"
                                        value={this.state.channel_id}
                                    />
                                </div>
                                {this.state.error && <div className="alert alert-danger">{this.state.error}</div>}
                            </div>
                            <input type="submit" value="Fetch Last Signed State" className="btn btn-primary" />
                        </form>
                        {(this.state.channel_id !== '') && this.state.lastState && <div className="alert alert-danger"><ShowState state={JSON.parse(this.state.lastState)} /></div>}

                    </div>
                    <div className="mt-2" ></div>
                    <form id="form" className="mt-2" onSubmit={this.handleConfirmChannel}>
                        <div className="form-group">
                            <label htmlFor="channel_id">Channel Id</label>
                            <div className="field">
                                <input
                                    id="channel_id"
                                    onChange={event => this.setState({ channelId: event.target.value })}
                                    type="text"
                                    name="channel_id"
                                    className="form-control"
                                    value={this.state.channelId}
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <label htmlFor="Count">Count</label>
                            <div className="field">
                                <input
                                    id="Count"
                                    onChange={event => this.setState({ count: event.target.value })}
                                    type="text"
                                    name="Count"
                                    className="form-control"
                                    value={this.state.count}
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <label htmlFor="aliceCash">Alice Cash</label>
                            <div className="field">
                                <input
                                    id="aliceCash"
                                    type="text"
                                    onChange={event => this.setState({ aliceCash: event.target.value })}
                                    name="aliceCash"
                                    className="form-control"
                                    value={this.state.aliceCash}
                                />
                            </div>
                            {/* {this.state.amountError && <div className="alert alert-danger">{this.state.amountError}</div>} */}
                        </div>
                        <div className="form-group">
                            <label htmlFor="bobCash">Bob Cash</label>
                            <div className="field">
                                <input
                                    id="bobCash"
                                    type="text"
                                    onChange={event => this.setState({ bobCash: event.target.value })}
                                    name="bobCash"
                                    className="form-control"
                                    value={this.state.bobCash}
                                />
                            </div>
                            {this.state.errors && <div className="alert alert-danger">{this.state.errors}</div>}
                        </div>
                        <input type="submit" value="Submit Transaction" className="btn btn-primary" />
                    </form>
                </div>
            </div >
        );
    }
};

export default CreateTransaction;
