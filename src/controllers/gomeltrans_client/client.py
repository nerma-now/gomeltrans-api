from typing import Union
from config import settings
from http import HTTPStatus
from pydantic import HttpUrl
from async_lru import alru_cache
from .enums import TypeTransport
from src.schemas.route import Route, Routes
from .exceptions import RouteNotFoundException
from src.schemas.stop import RouteStop, RouteStops
from src.controllers.http_client.client import HTTPClient
from bs4 import BeautifulSoup, ResultSet, SoupStrainer, Tag


class GomelTransClient(HTTPClient):
    def __init__(self,
                 base_url: HttpUrl = settings.gomeltrans.base_url):
        super().__init__()

        self._base_url = base_url

    @alru_cache
    async def get_routes(self,
                         type_transport: TypeTransport):
        url: str = self._base_url.__str__() + \
            'routes/{type_transport}'.format(
                type_transport=type_transport
            )

        async with HTTPClient() as http_client:
            response, status = await http_client.get(
                url=url
            )

            strainer: SoupStrainer = SoupStrainer(
                name='td',
                class_='content'
            )
            soup: BeautifulSoup = BeautifulSoup(
                markup=response,
                features='lxml',
                parse_only=strainer
            )

            routes_list: ResultSet = soup.find_all(
                name='div'
            )

            routes: list[Route] = list()

            for route in routes_list:
                b_element: Tag = route.find('b')
                number: str = b_element.text

                i_element: Union[Tag | str] = str()
                days: str = str()
                if i_element:
                    i_element = route.find('i')
                    days = i_element.text

                a_element: Tag = route.find('a')
                name: str = a_element.text \
                    .replace(number, str()).replace(days, str()).replace('—', '→')
                href: str = a_element.get('href')

                routes.append(
                    Route(
                        number=number,
                        name=name,
                        href=href,
                    )
                )

            return Routes(
                routes=routes
            )

    @alru_cache
    async def get_route_stops(self,
                              type_transport: TypeTransport,
                              number: str) -> RouteStops:
        url: str = self._base_url.__str__() + \
            'routes/{type_transport}/{number}'.format(
                type_transport=type_transport,
                number=number
            )

        async with HTTPClient() as http_client:
            response, status = await http_client.get(
                url=url
            )

            if status == HTTPStatus.NOT_FOUND:
                raise RouteNotFoundException(
                    'Route not found'
                )

        strainer: SoupStrainer = SoupStrainer(
            name='td',
            class_='content'
        )
        soup: BeautifulSoup = BeautifulSoup(
            markup=response,
            features='lxml',
            parse_only=strainer
        )

        td_tags: list[str] = ['t-left', 't-right']
        td_stops: list[ResultSet] = list()

        for td_tag in td_tags:
            td_stops.append(soup.find(
                name='td',
                class_=td_tag,
            ).select(
                selector='td[class=stop-name]'
            ))

        in_stops: list[RouteStop] = [RouteStop(
            name=stop.text.strip(),
            href=stop.find('a').get('href'),
        ) for stop in td_stops[0]]

        out_stops: list[RouteStop] = [RouteStop(
            name=stop.text.strip(),
            href=stop.find('a').get('href'),
        ) for stop in td_stops[1]]

        return RouteStops(
            in_stops=in_stops,
            out_stops=out_stops
        )

gomeltrans_client: GomelTransClient = GomelTransClient()