import React from 'react';
import { contract_address, contract_abi } from "./contract_config";
// import { Web3 } from "web3";


// const Tx = require('ethereumjs-tx')
const Web3 = require('web3')
const web3 = new Web3(new Web3(new Web3.providers.HttpProvider("http://localhost:8545")))

const sideChainContract = new web3.eth.Contract(contract_abi, contract_address)
let details_div = ""

const ShowDetails = async (props) => {
    // function startExit( bytes prevTx, bytes prevTxProof, uint prevTxBlkNum, bytes tx, bytes txProof, uint txBlkNum)
    try {
        var details = await sideChainContract.methods.getChannel(18).call()
        console.log('Alice', details['alice']['id'], details['alice']['cash'], details['alice']['waitForInput']);
        console.log('Bob', details['alice']['id'], details['alice']['cash'], details['alice']['waitForInput']);
        console.log('timeout', details['timeout']);
        console.log('status', details['status']);
        console.log('lastCount', details['publish_tx_count']);
        console.log('Money', details['money']);
        details_div = 'Alice ' + details['alice']['id'] + ' ' + details['alice']['cash'] + ' ' + details['alice']['waitForInput'] + '\n';
        details_div += 'Bob ' + details['alice']['id'] + ' ' + details['alice']['cash'] + ' ' + details['alice']['waitForInput'] + '\n';
        details_div += 'timeout ' + details['timeout'] + '\n';
        details_div += 'status ' + details['status'] + '\n';
        details_div += 'lastCount ' + details['publish_tx_count'] + '\n';
        details_div += 'Money ' + details['money'] + '\n';
        console.log(details_div)
    } catch (error) {
        console.log("startExit to given contract address reverted")
        console.log(error)
    }
}

const XYZ = () => {
    return (
        <div>
            <div className="App-content">
                <button onClick={ShowDetails}> ShowDetails</button>
                <div>
                    {details_div}
                </div>
            </div>
        </div>
    );

};

export default XYZ;