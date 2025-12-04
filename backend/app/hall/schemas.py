from pydantic import BaseModel

class HallSchema(BaseModel):
    id: int
    name: str
    capacity: int

    class Config:
        from_attributes = True