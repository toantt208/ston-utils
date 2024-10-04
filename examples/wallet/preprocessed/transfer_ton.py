from stonutils.client import TonapiClient
from stonutils.wallet import PreprocessedWalletV2R1
from stonutils.wallet.data import TransferData

# API key for accessing the Tonapi (obtainable from https://tonconsole.com)
API_KEY = ""

# Set to True for test network, False for main network
IS_TESTNET = True

# Mnemonic phrase for creating the wallet
MNEMONIC: list[str] = []


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, public_key, private_key, mnemonic = PreprocessedWalletV2R1.from_mnemonic(client, MNEMONIC)

    tx_hash = await wallet.batch_transfer(
        data_list=[
            TransferData(
                destination="UQ...",
                amount=0.01,
                body="Hello from tonutils!",
            ),
            TransferData(
                destination="UQ...",
                amount=0.01,
                body="Hello from tonutils!",
            ),
            TransferData(
                destination="UQ...",
                amount=0.01,
                body="Hello from tonutils!",
            ),
            TransferData(
                destination="UQ...",
                amount=0.01,
                body="Hello from tonutils!",
            ),
        ]
    )

    print("Successfully transferred!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
