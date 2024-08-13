// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

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