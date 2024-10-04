from stonutils.client import TonapiClient
from stonutils.nft import NFTEditable
from stonutils.nft.content import NFTOffchainContent
from stonutils.wallet import WalletV4R2

# API key for accessing the Tonapi (obtainable from https://tonconsole.com)
API_KEY = ""

# Set to True for test network, False for main network
IS_TESTNET = True

# Mnemonic phrase used to connect the wallet
MNEMONIC: list[str] = []

# Address of the NFT to be edited
NFT_ADDRESS = "EQ..."

# Suffix URI of the NFT metadata
SUFFIX_URI = f"new-content.json"


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    body = NFTEditable.build_edit_content_body(
        content=NFTOffchainContent(suffix_uri=SUFFIX_URI),
    )

    tx_hash = await wallet.transfer(
        destination=NFT_ADDRESS,
        amount=0.02,
        body=body,
    )

    print(f"Successfully edited the content of NFT at address: {NFT_ADDRESS}.")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
