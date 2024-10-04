from pytoniq_core import Address, begin_cell

from stonutils.client import TonapiClient
from stonutils.jetton import JettonMaster, JettonWallet
from stonutils.wallet import WalletV4R2

# API key for accessing the Tonapi (obtainable from https://tonconsole.com)
API_KEY = ""

# Set to True for the test network, False for the main network
IS_TESTNET = True

# Mnemonic phrase used to connect the wallet
MNEMONIC: list[str] = []

# The address of the Jetton Master contract
JETTON_MASTER_ADDRESS = "EQ..."

# Number of decimal places for the Jetton
JETTON_DECIMALS = 9

# Amount of Jettons to transfer (in base units, considering decimals)
JETTON_AMOUNT = 0.01

# The address of the recipient
DESTINATION_ADDRESS = "UQ..."

# Comment to include in the transfer payload
COMMENT = "Hello from tonutils!"


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    jetton_wallet_address = await JettonMaster.get_wallet_address(
        client=client,
        owner_address=wallet.address.to_str(),
        jetton_master_address=JETTON_MASTER_ADDRESS,
    )

    body = JettonWallet.build_transfer_body(
        recipient_address=Address(DESTINATION_ADDRESS),
        response_address=wallet.address,
        jetton_amount=int(JETTON_AMOUNT * (10 ** JETTON_DECIMALS)),
        forward_payload=(
            begin_cell()
            .store_uint(0, 32)  # Text comment opcode
            .store_snake_string(COMMENT)
            .end_cell()
        ),
        forward_amount=1,
    )

    tx_hash = await wallet.transfer(
        destination=jetton_wallet_address,
        amount=0.05,
        body=body,
    )

    print(f"Successfully transferred {JETTON_AMOUNT} jettons!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
