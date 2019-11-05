pragma solidity <0.6.0;

contract dataTypes {

    address myaddress;

    function assignaddress() public {
        myaddress = msg.sender;
        myaddress.balance;
        myaddress.transfer(10);
    }

    uint[10] myfixedaddr;

    uint[] myIntArr = [1, 2, 3];

    function arrfunc() public {
        myIntArr.push(1);
        myIntArr.length;
        myIntArr[0];
    }

    struct Account {
        uint balance;
        uint dailyLimit;
    }

    Account myaccount;

    function structfxn() public {
        myaccount.balance = 100;
    }

    mapping (address => Account) _account;

    function xe()  payable public {
        _account[msg.sender].balance += msg.value;
    }

    function getBalance() public view returns (uint) {
        return _account[msg.sender].balance;
    }
}