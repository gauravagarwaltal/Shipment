import { FetchAccount } from '../components/MetaMaskFetch';
const Web3 = require('web3')
const web3 = new Web3(Web3.givenProvider || "http://localhost:8545")


async function GenerateSignatures(count, aliceCash, bobCash) {

    // const hash = await web3.utils.soliditySha3(
    //     {type: 'address', value: vpc.options.address},
    //     {type: 'uint', value: sid},
    //     {type: 'uint', value: blockedAlice},
    //     {type: 'uint', value: blockedBob},
    //     {type: 'uint', value: version});

    const hash = await web3.utils.soliditySha3(
        { type: 'uint', value: count },
        { type: 'uint', value: aliceCash },
        { type: 'uint', value: bobCash });

    let sender = await FetchAccount()
    sender = web3.utils.toChecksumAddress(sender)
    console.log(sender)
    const sigAlice = await web3.eth.personal.sign(hash, sender, "");
    //web3.eth.sign(hash,aliceAddr);
    //web3.eth.sign(hash,bobAddr);
    return sigAlice
}


export default GenerateSignatures;