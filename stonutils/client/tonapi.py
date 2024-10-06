from typing import Any, List, Optional

from pytoniq_core import Cell

from ._base import Client
from ..account import AccountStatus, RawAccount


class TonapiClient(Client):
    """
    TonapiClient class for interacting with the TON blockchain.

    This class provides methods to run get methods and send messages to the blockchain,
    with options for network selection.
    """

    def __init__(
            self,
            api_key: Optional = None,
            is_testnet: Optional[bool] = False,
            base_url: Optional[str] = None,
    ) -> None:
        """
        Initialize the TonapiClient.

        :param api_key: The API key for accessing the Tonapi service.
            You can get API key here: https://tonconsole.com.
        :param is_testnet: Flag to indicate if testnet configuration should be used. Defaults to False.
        :param base_url: Optional base URL for the Tonapi service. If not provided,
            the default public URL will be used. You can specify your own API URL if needed.
        """
        if base_url is None:
            base_url = "https://tonapi.io" if not is_testnet else "https://testnet.tonapi.io"

        headers = {}
        if api_key:
            headers = {"Authorization": f"Bearer {api_key}"}

        super().__init__(base_url=base_url, headers=headers)

    async def run_get_method(
            self,
            address: str,
            method_name: str,
            stack: Optional[List[Any]] = None,
    ) -> Any:
        method = f"/v2/blockchain/accounts/{address}/methods/{method_name}"

        if stack:
            query_params = '&'.join(f"args={arg}" for arg in stack)
            method = f"{method}?{query_params}"

        return await self._get(method=method)

    async def send_message(self, boc: str) -> None:
        method = "/v2/blockchain/message"

        await self._post(method=method, body={"boc": boc})

    async def get_raw_account(self, address: str) -> RawAccount:
        method = f"/v2/blockchain/accounts/{address}"
        result = await self._get(method=method)

        code = Cell.one_from_boc(result["code"])
        data = Cell.one_from_boc(result["data"])

        return RawAccount(
            balance=int(result["balance"]),
            code=code,
            data=data,
            status=AccountStatus(result["status"]),
            last_transaction_lt=int(result["last_transaction_lt"]),
            last_transaction_hash=result["last_transaction_hash"],
        )

    async def get_account_balance(self, address: str) -> int:
        raw_account = await self.get_raw_account(address)

        return raw_account.balance
