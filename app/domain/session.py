from pydantic import BaseModel
from typing import Optional

class Session(BaseModel):
    id: str
    scenario_id: str
    current_step: Optional[str] = None
    is_ended: bool = False
