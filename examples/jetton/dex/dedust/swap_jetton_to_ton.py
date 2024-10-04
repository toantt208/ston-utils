from stonutils.client import TonapiClient
from stonutils.jetton import JettonMaster, JettonWallet
from stonutils.jetton.dex.dedust import Asset, Factory, PoolType
from stonutils.wallet import WalletV4R2

# API key for accessing the Tonapi (obtainable from https://tonconsole.com)
API_KEY = ""

# Mnemonic phrase used to connect the wallet
MNEMONIC: list[str] = []

# Address of the Jetton Master contract
JETTON_MASTER_ADDRESS = "EQ..."

# Number of decimal places for the Jetton
JETTON_DECIMALS = 9

# Amount of Jettons to swap (in base units, considering decimals)
JETTON_AMOUNT = 0.01


async def main() -> None:
    client = TonapiClient(api_key=API_KEY)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    factory = Factory(client)
    pool = await factory.get_pool(
        pool_type=PoolType.VOLATILE,
        assets=[
            Asset.native(),
            Asset.jetton(JETTON_MASTER_ADDRESS),
        ],
    )
    jetton_vault = await factory.get_jetton_vault(JETTON_MASTER_ADDRESS)
    jetton_wallet_address = await JettonMaster.get_wallet_address(
        client=client,
        owner_address=wallet.address.to_str(),
        jetton_master_address=JETTON_MASTER_ADDRESS,
    )

    tx_hash = await wallet.transfer(
        destination=jetton_wallet_address,
        amount=0.3,
        body=JettonWallet.build_transfer_body(
            recipient_address=jetton_vault.address,
            jetton_amount=int(JETTON_AMOUNT * (10 ** JETTON_DECIMALS)),
            response_address=wallet.address,
            forward_payload=jetton_vault.create_swap_payload(pool.address),
            forward_amount=int(0.25 * 1e9),
        ),
    )

    print("Successfully swapped Jetton to TON!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
