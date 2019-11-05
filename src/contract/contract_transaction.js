import { contract_address, contract_abi } from "./contract_config";
// import { Web3 } from "web3";
// import { aliceAddress } from "./wallet";
import { FetchAccount } from '../components/MetaMaskFetch';
import { toast } from 'react-toastify';

const Web3 = require('web3')
const web3 = new Web3(Web3.givenProvider || "http://localhost:8545")
const sideChainContract = new web3.eth.Contract(contract_abi, contract_address)

const GetChannelDetails = async (channelId) => {
    try {
        var details = await sideChainContract.methods.getChannel(channelId).call()
        let details_div = {
            'Alice Id': details['alice']['id'],
            'Alice Cash': details['alice']['cash'],
            'Alice Input Flag': String(details['alice']['waitForInput']),
            'Bob Id': details['bob']['id'],
            'Bob Cash': details['bob']['cash'],
            'Bob Input Flag': String(details['bob']['waitForInput']),
            'Timeout': details['timeout'],
            'Status': details['status'],
            'Published Tx Count': details['publish_tx_count'],
            'Money': details['money']
        }
        return details_div;
    } catch (error) {
        console.log("contract details are tempered or connectivity issue")
        console.log(error)
    }
}

const FetchOtherParty = async (channelId, ownAddress) => {
    try {
        var details = await sideChainContract.methods.getChannel(channelId).call()
        // console.log(details)
        if (web3.utils.toChecksumAddress(ownAddress) === web3.utils.toChecksumAddress(details['alice']['id'])) {
            return web3.utils.toChecksumAddress(details['bob']['id'])
        }
        else {
            return web3.utils.toChecksumAddress(details['alice']['id'])
        }
    } catch (error) {
        console.log("contract details are tempered or connectivity issue")
        console.log(error)
    }
}

const ChannelExists = async (channelId) => {
    let details = await GetChannelDetails(channelId)
    return /^0x0+$/.test(details['Alice Id']);
}

const CreateNewChannel = async (channelId, theOtherParty) => {
    const sender = await FetchAccount()
    console.log(sender, web3.utils.checkAddressChecksum(sender))
    try {
        var txHash = await sideChainContract.methods.openChannel(channelId, web3.utils.toChecksumAddress(theOtherParty))
            .send({ from: web3.utils.toChecksumAddress(sender), gas: 200000 })
        console.log('new channel created, txHash->', txHash.transactionHash);
    } catch (error) {
        console.log("Open Channel request reverted")
        console.log(error)
    }
}

const ChannelConfirm = async (channelId, cash) => {
    try {
        const sender = await FetchAccount()
        let flag = await ChannelExists(channelId)
        if (flag) {
            toast.error(`Channel with ${channelId} doesn't exists`)
        } else {
            var txHash = await sideChainContract.methods.confirm(channelId)
                .send({ from: web3.utils.toChecksumAddress(sender), value: web3.utils.toHex(web3.utils.toWei(cash, 'wei')), gas: 200000 })
            console.log('Channel Deposit Confirmed. txHash-> ', txHash.transactionHash);
            toast.success("Deposit confirmed")
        }
    } catch (error) {
        console.log("Channel Deposit request reverted")
        console.log(error)
        toast.error(`Deposit Declined for Channel Id ${channelId}`)
    }
}

const ChannelRefund = async (channelId, self) => {
    try {
        var txHash = await sideChainContract.methods.refund(channelId)
            .send({ from: web3.utils.toChecksumAddress(self), gas: 200000 })
        console.log('Channel Refund Confirmed. txHash-> ', txHash.transactionHash);
    } catch (error) {
        console.log("Channel Refund request reverted")
        console.log(error)
    }
}

const IsValidSignature = async (addr, count, sender_balance, recipient_balance, signature) => {
    try {
        addr = web3.utils.toChecksumAddress(addr)
        var flag = await sideChainContract.methods.isValidSignature(addr, count, sender_balance, recipient_balance, signature).call()
        console.log('isValidSignature ', flag);
        return flag
    } catch (error) {
        console.log("contract details are tempered or connectivity issue or invalid arguments passed")
        console.log(error)
    }
}

const ChannelFinalizeClose = async (channelId, self) => {
    try {
        var txHash = await sideChainContract.methods.finalizeClose(channelId)
            .send({ from: web3.utils.toChecksumAddress(self), gas: 200000 })
        console.log('Channel Closed. txHash-> ', txHash.transactionHash);
    } catch (error) {
        console.log("Channel finalizeClose request reverted")
        console.log(error)
    }
}

const ChannelClose = async (channel_id, count, sender_balance, recipient_balance, signature, self) => {
    try {
        var txHash = await sideChainContract.methods.close(channel_id, count, sender_balance, recipient_balance, signature)
            .send({ from: web3.utils.toChecksumAddress(self), gas: 200000 })
        console.log('Channel Close request proceed. txHash-> ', txHash.transactionHash);
    } catch (error) {
        console.log("Channel Closed request reverted")
        console.log(error)
    }
}

const GetReceipt = async () => {
    console.log(await web3.eth.getTransactionReceipt("0x71a6cbe5ff2dc219d12149e1986c584e6a3ef094a18177dd831a24466d2b1ffc"))

}

export { GetChannelDetails, FetchOtherParty, ChannelExists, CreateNewChannel, ChannelConfirm, ChannelRefund, IsValidSignature, ChannelFinalizeClose, ChannelClose, GetReceipt }