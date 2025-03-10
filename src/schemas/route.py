from pydantic import BaseModel


class Route(BaseModel):
    name: str
    number: str
    href: str

class Routes(BaseModel):
    routes: list[Route]