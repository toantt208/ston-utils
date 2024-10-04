from stonutils.client import TonapiClient
from stonutils.jetton import JettonMaster
from stonutils.wallet import WalletV4R2

# API key for accessing the Tonapi (obtainable from https://tonconsole.com)
API_KEY = ""

# Set to True for test network, False for main network
IS_TESTNET = True

# Mnemonic phrase used to connect the wallet
MNEMONIC: list[str] = []

# The address of the Jetton Master contract
JETTON_MASTER_ADDRESS = "EQ..."

# The amount of Jettons to mint (in base units, considering decimals)
JETTON_AMOUNT = 1000000

# Number of decimal places for the Jetton
JETTON_DECIMALS = 9


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    body = JettonMaster.build_mint_body(
        destination=wallet.address,
        jetton_amount=int(JETTON_AMOUNT * (10 ** JETTON_DECIMALS)),
    )

    tx_hash = await wallet.transfer(
        destination=JETTON_MASTER_ADDRESS,
        amount=0.05,
        body=body,
    )

    print(f"Successfully minted {JETTON_AMOUNT} Jettons!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
