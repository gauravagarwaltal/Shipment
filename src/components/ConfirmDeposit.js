import React from 'react';
import { ChannelConfirm } from '../contract/contract_transaction';
// import { toast } from 'react-toastify'

class ConfirmDeposit extends React.Component {
    state = {
        channelId: "",
        channelIdError: "",
        amount: '',
        amountError: "",
    };

    handleConfirmChannel = async (event) => {
        event.preventDefault();
        this.setState({ 'channelIdError': "" })
        this.setState({ 'amountError': "" })
        if (Number.isNaN(parseInt(this.state.channelId, 10))) {
            this.setState({ 'channelIdError': "Enter Interger channel Id" })
        }
        else if (Number.isNaN(parseInt(this.state.amount, 10))) {
            this.setState({ 'amountError': "Enter Integer amount(in wei unit)" })
        }
        else {
            ChannelConfirm(this.state.channelId, this.state.amount)
        }
        this.setState({ 'channelId': "" })
        this.setState({ 'amount': "" })
    }

    render() {
        return (
            <div>
                <form id="form" onSubmit={this.handleConfirmChannel}>
                    <div className="form-group">
                        <label htmlFor="channelId">Channel Id</label>
                        <div className="field">
                            <input
                                id="channelId"
                                type="text"
                                onChange={event => this.setState({ channelId: event.target.value })}
                                name="channelId"
                                className="form-control"
                                value={this.state.channelId}
                            />
                        </div>
                        {this.state.channelIdError && <div className="alert alert-danger">{this.state.channelIdError}</div>}
                    </div>
                    <div className="form-group">
                        <label htmlFor="amount">Amount</label>
                        <div className="field">
                            <input
                                id="amount"
                                type="text"
                                onChange={event => this.setState({ amount: event.target.value })}
                                name="amount"
                                className="form-control"
                                value={this.state.amount}
                            />
                        </div>
                        {this.state.amountError && <div className="alert alert-danger">{this.state.amountError}</div>}
                    </div>
                    <input type="submit" value="Deposit Amount" className="btn btn-primary" />
                </form>
            </div>
        )
    }
}


export default ConfirmDeposit;