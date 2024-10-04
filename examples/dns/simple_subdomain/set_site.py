from stonutils.client import TonapiClient
from stonutils.dns.simple_subdomain import SubdomainManager
from stonutils.wallet import WalletV4R2

# API key for accessing the Tonapi (obtainable from https://tonconsole.com)
API_KEY = ""

# Set to True for test network, False for main network
IS_TESTNET = True

# Mnemonic phrase used to connect the wallet
MNEMONIC: list[str] = []

# The address of the subdomain manager contract
SUBDOMAIN_MANAGER_ADDRESS = "EQ..."

# The ADNL address to be set for the subdomain
ADNL_ADDRESS = "{hex}"

# The subdomain to be registered
SUBDOMAIN = "example"


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    body = SubdomainManager.build_set_site_record_body(SUBDOMAIN, ADNL_ADDRESS)

    tx_hash = await wallet.transfer(
        destination=SUBDOMAIN_MANAGER_ADDRESS,
        amount=0.02,
        body=body,
    )

    print("Subdomain successfully registered and site record set!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
