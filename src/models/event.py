from pydantic import BaseModel


class Event(BaseModel):
    object_type: str
    object_id: int
    aspect_type: str
    updates: dict
    owner_id: int
    subscription_id: int
    event_time: int
