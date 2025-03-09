from typing import List
from pydantic import BaseModel


class RouteStop(BaseModel):
    name: str
    href: str

class RouteStops(BaseModel):
    in_stops: List[RouteStop]
    out_stops: List[RouteStop]