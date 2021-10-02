// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;


contract Overflow {
    
    function overflow() public view returns(uint8) {
        uint8 big = 255 + uint8(100);
        return big;
    }
}