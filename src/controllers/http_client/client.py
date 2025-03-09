from http import HTTPStatus
from aiohttp import ClientSession
from typing import Optional, Self
from validators import url as url_validator
from .exceptions import (HTTPClientException,
                         UrlValidateException)


class HTTPClient:
    def __init__(self) -> None:
        """
        Initializing an instance

        :return: None
        """

        self.__session: Optional[ClientSession] = None

    def __session_getter(self) -> ClientSession:
        """
        Session acquisition method

        :return: ClientSession
        """

        if self.__session is None:
            self.__session = ClientSession()
        return self.__session

    async def __aenter__(self) -> Self:
        """
        Method to get session in asynchronous context

        :return: Self
        """

        return self

    async def __aexit__(self,
                        exc_type,
                        exc_val,
                        exc_tb) -> None:
        """
        Method to close session in asynchronous context

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: None
        """

        if self.__session is not None:
            await self.__session.close()

    async def get(self,
                  url: str) -> tuple[bytes, HTTPStatus]:
        """
        Method to get url

        :param url: str
        :return: tuple[bytes, HTTPStatus]
        """

        if not url_validator(url):
            raise UrlValidateException(
                'Invalid URL'
            )

        try:
            async with self.__session_getter().get(
                    url=url
            ) as get:
                response: bytes = await get.read()
                return response, HTTPStatus(get.status)
        except Exception as e:
            raise HTTPClientException(e)