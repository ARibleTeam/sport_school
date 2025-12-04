from pydantic import BaseModel
import datetime

class TrainingSchema(BaseModel):
    id: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    is_group_training: bool

    class Config:
        from_attributes = True