from stonutils.client import TonapiClient
from stonutils.wallet import WalletV4R2
from stonutils.wallet.data import TransferJettonData

# API key for accessing the Tonapi (obtainable from https://tonconsole.com)
API_KEY = ""

# Set to True for test network, False for main network
IS_TESTNET = True

# Mnemonic phrase for creating the wallet
MNEMONIC: list[str] = []


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, public_key, private_key, mnemonic = WalletV4R2.from_mnemonic(client, MNEMONIC)

    tx_hash = await wallet.batch_jetton_transfer(
        data_list=[
            TransferJettonData(
                destination="UQ...",
                jetton_master_address="EQ...",
                jetton_amount=0.01,
                jetton_decimals=9,
                forward_payload="Hello from tonutils!",
            ),
            TransferJettonData(
                destination="UQ...",
                jetton_master_address="EQ...",
                jetton_amount=0.01,
                jetton_decimals=9,
                forward_payload="Hello from tonutils!",
            ),
            TransferJettonData(
                destination="UQ...",
                jetton_master_address="EQ...",
                jetton_amount=0.01,
                jetton_decimals=9,
                forward_payload="Hello from tonutils!",
            ),
            TransferJettonData(
                destination="UQ...",
                jetton_master_address="EQ...",
                jetton_amount=0.01,
                jetton_decimals=9,
                forward_payload="Hello from tonutils!",
            ),
        ]
    )

    print("Successfully transferred!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
