from pydantic import BaseModel
from typing import Optional

class ChildHealthProfile(BaseModel):
    name: Optional[str] = None
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    sleep_hours: float
    screen_time_hours: float
    physical_activity_level: str
    eating_habits: str
    mood: str
    symptoms: Optional[str] = None