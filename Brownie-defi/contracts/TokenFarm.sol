//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "@openzeppelin/contracts/access/Ownable.sol";

contract TokenFarm is Ownable {
    uint256 public allowedAmountToStake = 0;
    address[] public allowedTokens;

    function stakeTokens(uint256 _amount, address _token) public {
        require(
            _amount > allowedAmountToStake,
            "Amount must be gretter then 0"
        );
        require(isAllowedToken(_token), "Oops this token is not allowed!");
    }

    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function isAllowedToken(address _token) public returns (bool) {
        for (uint256 i = 0; i < allowedTokens.length; i++) {
            if (allowedTokens[i] == _token) {
                return true;
            } else {
                return false;
            }
        }
    }
}
