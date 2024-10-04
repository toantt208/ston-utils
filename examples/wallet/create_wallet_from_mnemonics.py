from stonutils.client import TonapiClient
from stonutils.wallet import (
    # WalletV3R1,
    # Uncomment the following lines to use different wallet versions:
    # WalletV3R2,
    # WalletV4R1,
    # WalletV4R2,
    WalletV5R1,
    # HighloadWalletV2,
    # HighloadWalletV3,
    # PreprocessedWalletV2,
    # PreprocessedWalletV2R1,
)

# API key for accessing the Tonapi (obtainable from https://tonconsole.com)
API_KEY = ""

# Mnemonic phrase for wallet creation
MNEMONIC = ""
# Set to True for test network, False for main network
IS_TESTNET = True


def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)

    wallet, public_key, private_key, mnemonic = WalletV5R1.from_mnemonic(
        mnemonic=MNEMONIC,
        client=client,
    )

    address = wallet.address.to_str(
        is_bounceable=False,
        is_test_only=IS_TESTNET,
    )
    print("Wallet has been successfully created!")
    print(f"Address: {address}")
    print(f"Mnemonic: {mnemonic}")

    # seqno = WalletV5R1.get_seqno(
    #     client=client,
    #     address=address,
    # )
    # print(f"Wallet seqno: {seqno}")

    # txHash = wallet.transfer(
    #     destination=""
    # )
    # transfer to wallet



if __name__ == "__main__":
    main()
