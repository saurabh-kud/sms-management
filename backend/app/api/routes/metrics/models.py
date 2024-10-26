from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    country: Optional[str] =None

