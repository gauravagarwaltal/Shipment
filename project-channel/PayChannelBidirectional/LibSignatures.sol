pragma solidity ^0.4.0;

import "./ILibSignatures.sol";

contract LibSignatures is ILibSignatures {
    event EventVerificationSucceeded(bytes Signature, bytes32 Message, address Key);
    event EventVerificationFailed(bytes Signature, bytes32 Message, address Key);

    /*
    * This functionality verifies ECDSA signatures
    * @returns true if the signature of addr over message is correct
    */
    function verify(address addr, bytes32 message, bytes signature) public view returns(bool) {
        if (signature.length != 65)
            return (false);

        bytes32 r;
        bytes32 s;
        uint8 v;

        assembly {
            r := mload(add(signature, 32))
            s := mload(add(signature, 64))
            v := byte(0, mload(add(signature, 96)))
        }

        if (v < 27)
            v += 27;

        if (v != 27 && v != 28)
            return (false);

        address pk = ecrecover(message, v, r, s);

        if (pk == addr) {
            return (true);
        } else {
            return (false);
        }
    }

    function CheckSignature(address verifier, uint vid, address p1, uint cash1, uint subchan1, address Ingrid,
                                    uint version, bytes sig) public view returns (bool) {
        bytes32 msgHash = keccak256(vid, p1, cash1, subchan1, Ingrid, version);
        bytes memory prefix = "\x19Ethereum Signed Message:\n32";
        bytes32 prefixedHash = keccak256(prefix, msgHash);
        return verify(verifier, prefixedHash, sig);
    }

    function getNow() public view returns (uint) {
        return now;
    }

    function checkHash(uint vid, address p1, uint cash1, uint subchan1, address Ingrid,
                                    uint version) public pure returns (bytes32) {
        return keccak256(vid, p1, cash1, subchan1, Ingrid, version);

    }
}
