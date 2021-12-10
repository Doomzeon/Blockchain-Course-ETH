// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;

    enum LOTTERY_STATES {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATES public lottery_state;
    uint256 public fee;
    bytes32 keyHash;
    address payable public recentWinner;
    uint256 public randomness;

    constructor(
        address _priceFeedAddress,
        address _vrfCordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCordinator, _link) {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATES.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATES.OPEN);
        require(msg.value >= getEntranceFee(), "Not enought ETH");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustablePrice = uint256(price) * 10**10; //18 decimals like eth
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustablePrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATES.CLOSED,
            "Can not start a new lottery yet!"
        );
        lottery_state = LOTTERY_STATES.OPEN;
    }

    function endLottery() public onlyOwner {
        // uint256(
        //     keccack256(
        //         abi.encodePacked(
        //             nonce,
        //             msg.sender,
        //             block.difficulty,
        //             block.timestamp
        //         )
        //     )
        // ) % players.length;
        lottery_state = LOTTERY_STATES.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATES.CALCULATING_WINNER,
            "You are not there yet!"
        );
        require(_randomness > 0, "random-not-found");
        uint256 indeOfWinner = _randomness % players.length;
        recentWinner = players[indeOfWinner];
        recentWinner.transfer(address(this).balance);
        // Reset lottery
        players = new address payable[](0);
        lottery_state = LOTTERY_STATES.CLOSED;
        randomness = _randomness;
    }
}
