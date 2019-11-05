pragma solidity ^0.4.24;

import "./ILibSignatures.sol";

contract Channel {
    event EventInitializing(address addressAlice, address addressBob);
    event EventInitialized(uint cashAlice, uint cashBob);
    event EventRefunded();
    event EventClosing();
    event EventClosed();
    event EventNotClosed();

    modifier AliceOrBob { require(msg.sender == alice.id || msg.sender == bob.id); _;}

    //Data type for Internal Contract
    struct Party {
        address id;
        uint cash;
        bool waitForInput;
    }

    // State options
    enum ChannelStatus {Init, Open, InConflict, Settled, WaitingToClose, ReadyToClose}

    // MSContract variables
    Party public alice;
    Party public bob;
    uint public timeout;
    ChannelStatus public status;
    uint public publish_tx_count;
    ILibSignatures libSig;

    /*
    * Constructor for setting initial variables takes as input
    * addresses of the parties of the basic channel
    */
    constructor(address _libSig, address _addressAlice, address _addressBob) public {
        // set addresses
        alice.id = _addressAlice;
        bob.id = _addressBob;

        // set limit until which Alice and Bob need to respond
        timeout = now + 100 minutes;
        alice.waitForInput = true;
        bob.waitForInput = true;

        libSig = ILibSignatures(_libSig);
        // set other initial values
        status = ChannelStatus.Init;
        publish_tx_count = 0;
        emit EventInitializing(_addressAlice, _addressBob);
    }

    /*
    * This functionality is used to send funds to the contract during 100 minutes after channel creation
    */
    function confirm() public AliceOrBob payable {
        require(status == ChannelStatus.Init && now < timeout);

        // Response (in time) from Player A
        if (alice.waitForInput && msg.sender == alice.id) {
            alice.cash = msg.value;
            alice.waitForInput = false;
        }

        // Response (in time) from Player B
        if (bob.waitForInput && msg.sender == bob.id) {
            bob.cash = msg.value;
            bob.waitForInput = false;
        }
        // execute if both players responded
        if (!alice.waitForInput && !bob.waitForInput) {
            status = ChannelStatus.Open;
            timeout = 0;
            emit EventInitialized(alice.cash, bob.cash);
        }
    }

    /*
    * This function is used in case one of the players did not confirm the MSContract in time
    */
    function refund() public AliceOrBob {
        require(status == ChannelStatus.Init && now > timeout);

        // refund money
        if (!alice.waitForInput && alice.cash > 0) {
            require(alice.id.send(alice.cash));
        }
        if (!bob.waitForInput && bob.cash > 0) {
            require(bob.id.send(bob.cash));
        }
        emit EventRefunded();

        // terminate contract
        selfdestruct(alice.id);
    }


    function isValidSignature(address addr, uint count, uint sender_balance, uint recipient_balance, bytes signature)
        public
        view
        returns (bool)
    {
        // bytes32 message = keccak256(abi.encodePacked(count, sender_balance, recipient_balance));
        bytes32 msgHash = keccak256(count, sender_balance, recipient_balance);
        bytes memory prefix = "\x19Ethereum Signed Message:\n32";
        bytes32 prefixedHash = keccak256(prefix, msgHash);
        return libSig.verify(addr, prefixedHash, signature);
    }

    /*
    * This function is used in case one of the players did not confirm the state
    */
    /*
    * This functionality closes the channel when there is no internal machine
    */
    function close(uint count, uint sender_balance, uint recipient_balance, bytes signature) public AliceOrBob {
        if (status == ChannelStatus.Open) {
            if ( msg.sender == alice.id)
                require(isValidSignature(bob.id, count, sender_balance, recipient_balance, signature));
            else
                require(isValidSignature(alice.id, count, sender_balance, recipient_balance, signature));
            // if _balance > address(this).balance, send address(this).balance to recipient
            require(sender_balance + recipient_balance == address(this).balance);
            require(count >= publish_tx_count);

            publish_tx_count = count;
            bob.cash = recipient_balance;

            status = ChannelStatus.WaitingToClose;
            timeout = now + 300 minutes;
            alice.waitForInput = true;
            bob.waitForInput = true;
            emit EventClosing();
        }

        if (status != ChannelStatus.WaitingToClose) return;

        // Response (in time) from Player A
        if (alice.waitForInput && msg.sender == alice.id)
            alice.waitForInput = false;

        // Response (in time) from Player B
        if (bob.waitForInput && msg.sender == bob.id)
            bob.waitForInput = false;

        if (!alice.waitForInput && !bob.waitForInput) {
            // send funds to A and B
            if (bob.id.send(bob.cash)) bob.cash = 0;

            // terminate channel
            if (bob.cash == 0) {
                emit EventClosed();
                selfdestruct(alice.id);
            }
        }
    }

    function finalizeClose() public AliceOrBob {
        if (status != ChannelStatus.WaitingToClose) {
            emit EventNotClosed();
            return;
        }

        // execute if timeout passed
        if (now > timeout) {
            // send funds to A and B
            if (alice.id.send(alice.cash)) alice.cash = 0;
            if (bob.id.send(bob.cash)) bob.cash = 0;

            // terminate channel
            if (alice.cash == 0 && bob.cash == 0) {
                emit EventClosed();
                selfdestruct(alice.id);
            }
        }
    }
}