from app.api.routes.sessions.models import SessionRequest
from typing import Optional



class CountryOperatorPairRequest(SessionRequest):
    priority: Optional[str] =None
    

