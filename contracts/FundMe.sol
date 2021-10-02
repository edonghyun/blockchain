// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";


contract FundMe {
    AggregatorV3Interface internal priceFeed;
    
    constructor() {
        priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
    }


    mapping(address => uint256) public addressToAmountFunded;
    
    function fund() public payable {
        addressToAmountFunded[msg.sender] += msg.value;
    }
    
    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }
        
    function getPrice() public view returns (uint256) {
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(3);
    }
    
    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount);
        return ethPrice;
    }
    
    function getLatestPrice() public view returns (int) {
        (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return price;
    }
    
}