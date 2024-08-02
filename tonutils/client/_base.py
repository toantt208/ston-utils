import json
from typing import Any, Optional, List, Dict

import aiohttp


class Client:
    """
    Base client class for interacting with the TON blockchain.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.base_url = kwargs.get("base_url", "")
        self.headers = kwargs.get("headers", {})
        self.timeout = kwargs.get("timeout", 10)

    @staticmethod
    async def __read_content(response: aiohttp.ClientResponse) -> Any:
        """
        Read the response content.

        :param response: The HTTP response object.
        :return: The response content.
        """
        try:
            data = await response.read()
            try:
                content = json.loads(data.decode())
            except json.JSONDecodeError:
                content = data.decode()
        except aiohttp.ClientPayloadError as e:
            content = {"error": f"Payload error occurred: {e}"}
        except Exception as e:
            raise aiohttp.ClientError(f"Failed to read response content: {e}")

        return content

    async def _request(
            self,
            method: str,
            path: str,
            headers: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request.

        :param method: The HTTP method (GET or POST).
        :param path: The API path.
        :param headers: Optional headers to include in the request.
        :param params: Optional query parameters.
        :param body: Optional request body data.
        :return: The response content as a dictionary.
        """
        url = self.base_url + path
        self.headers.update(headers or {})
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.request(
                        method=method,
                        url=url,
                        params=params,
                        json=body,
                        timeout=self.timeout,
                ) as response:
                    content = await self.__read_content(response)

                    if not response.ok:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=content.get("error", content)
                        )

                    return content

        except aiohttp.ClientError:
            raise

    async def _get(
            self,
            method: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a GET request.

        :param method: The API method.
        :param params: Optional query parameters.
        :param headers: Optional headers to include in the request.
        :return: The response content as a dictionary.
        """
        return await self._request("GET", method, headers, params=params)

    async def _post(
            self,
            method: str,
            params: Optional[Dict[str, Any]] = None,
            body: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a POST request.

        :param method: The API method.
        :param body: The request body data.
        :param headers: Optional headers to include in the request.
        :return: The response content as a dictionary.
        """
        return await self._request("POST", method, headers, params=params, body=body)

    async def run_get_method(
            self,
            address: str,
            method_name: str,
            stack: Optional[List[Any]] = None,
    ) -> Any:
        """
        Run a get method on a specified address in the blockchain.

        :param address: The address of the smart contract on the blockchain.
        :param method_name: The name of the method to run on the smart contract.
        :param stack: The stack of arguments to pass to the method. Defaults to None.
        :return: The result of the get method call.
        """
        raise NotImplementedError

    async def send_message(self, boc: str) -> None:
        """
        Send a message to the blockchain.

        :param boc: The bag of cells (BoC) string representation of the message to be sent.
        """
        raise NotImplementedError
