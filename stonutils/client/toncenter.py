import base64
from typing import Any, List, Optional, Union

from pytoniq_core import Cell, Address

from ._base import Client
from ..account import AccountStatus, RawAccount
from ..utils import boc_to_base64_string


class ToncenterClient(Client):
    """
    ToncenterClient class for interacting with the TON blockchain.

    This class provides methods to run get methods and send messages to the blockchain,
    with options for network selection.
    """

    def __init__(
            self,
            api_key: str,
            is_testnet: Optional[bool] = False,
            base_url: Optional[str] = None,
    ) -> None:
        """
        Initialize the ToncenterClient.

        :param api_key: The API key for accessing the Toncenter service.
            You can get API key here: https://t.me/tonapibot
        :param is_testnet: Flag to indicate if testnet configuration should be used. Defaults to False.
        :param base_url: Optional base URL for the Toncenter API. If not provided,
            the default public URL will be used. You can specify your own API URL if needed.
        """
        if base_url is None:
            base_url = "https://toncenter.com" if not is_testnet else "https://testnet.toncenter.com"
        headers = {"X-Api-Key": api_key}

        super().__init__(base_url=base_url, headers=headers)

    async def run_get_method(
            self,
            address: str,
            method_name: str,
            stack: Optional[List[Any]] = None,
    ) -> Any:
        method = f"/api/v3/runGetMethod"
        body = {
            "address": address,
            "method": method_name,
            "stack": [
                {"type": "num", "value": str(v)}
                if isinstance(v, int) else
                {"type": "slice", "value": v}
                for v in (stack or [])
            ],
        }

        return await self._post(method=method, body=body)

    async def send_message(self, boc: str) -> None:
        method = "/api/v3/message"

        await self._post(method=method, body={"boc": boc_to_base64_string(boc)})

    async def get_raw_account(self, address: str) -> RawAccount:
        method = f"/api/v3/account"
        params = {"address": address}
        result = await self._get(method=method, params=params)

        code = Cell.one_from_boc(result["code"])
        data = Cell.one_from_boc(result["data"])

        return RawAccount(
            balance=int(result["balance"]),
            code=code,
            data=data,
            status=AccountStatus(result["status"]),
            last_transaction_lt=int(result["last_transaction_lt"]),
            last_transaction_hash=base64.b64decode(result["last_transaction_hash"]).hex(),
        )

    async def get_account_balance(self, address: str) -> int:
        raw_account = await self.get_raw_account(address)

        return raw_account.balance

    async def estimate_fee(
        self,
        address: str,
        body: str,
        init_code: str,
        init_data: str,
        ignore_chksig: bool = True,
    ):
        method = "/api/v3/estimateFee"
        body = {
            "address": str(address),
            "body": body,
            "init_code": init_code,
            "init_data": init_data,
            "ignore_chksig": 'true' if ignore_chksig else 'false',
        }
        result = await self._post(
            method=method,
            body=body,
        )

        return result