from pydantic import BaseModel


class SessionRequest(BaseModel):
    country: str
    operator: str

