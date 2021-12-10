// contracts/SimpleCollectible.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract SimpleCollectible is ERC721URIStorage {
    uint256 public tokenCounter;

    constructor() public ERC721("Amaz", "WTF") {
        tokenCounter = 0;
    }

    function createCollectible(string memory tokenUri)
        public
        returns (uint256)
    {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenUri);
        tokenCounter += 1;
        return newTokenId;
    }
}
