from pydantic import BaseModel


class APIResponse(BaseModel):
    status: int = 200
    message: str = "Data fetched successfully!!"
    data: object = None