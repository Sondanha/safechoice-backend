from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class EventType(str, Enum):
    CLICK = "click"
    INPUT = "input"
    SUBMIT = "submit"
    WAIT = "wait"

class Event(BaseModel):
    session_id: str
    type: EventType
    payload: dict
    timestamp: datetime
