from pydantic import BaseModel

class MetaInfoSchema(BaseModel):
    id: int
    name: str
    value: str
