from async_lru import alru_cache
from http import HTTPStatus
from pydantic import HttpUrl
from config import settings
from .enums import TypeTransport
from bs4 import BeautifulSoup, ResultSet
from src.schemas.stop import RouteStop, RouteStops
from src.controllers.http_client.client import HTTPClient
from .exceptions import RouteNotFoundException


class GomelTransClient(HTTPClient):
    def __init__(self,
                 base_url: HttpUrl = settings.gomeltrans.base_url):
        super().__init__()

        self._base_url = base_url

    @alru_cache(maxsize=32)
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
                    f'Route not found'
                )

        soup: BeautifulSoup = BeautifulSoup(
            markup=response,
            features='lxml')

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