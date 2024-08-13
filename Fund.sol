pragma solidity >= 0.8.11 <= 0.8.11;

contract Fund {
    string public users;
    string public bankaccount;

    function addUsers(string memory u) public {
        users = u;	
    }

    function getUsers() public view returns (string memory) {
        return users;
    }

    function bankAccount(string memory ba) public {
        bankaccount = ba;	
    }

    function getBankAccount() public view returns (string memory) {
        return bankaccount;
    }

    constructor() public {
        users = "empty";
	bankaccount = "empty";
    }
}