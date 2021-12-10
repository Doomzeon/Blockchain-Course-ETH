from scripts.utils import get_account
from brownie import SimpleCollectible

simple_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.png.json"
OPENSEA_URL = "https://testents.opensea.io/assets/{}/{}"


def main():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(
        simple_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"Ohh you can view nft at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter()-1)}")
