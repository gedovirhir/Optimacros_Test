from pydantic import BaseModel

class FactorialResponse(BaseModel):
    number: int
    result: int