from pydantic import BaseModel, validator
from decimal import Decimal

from typing import Union

class FactorialResponse(BaseModel):
    number: int
    result: Decimal
    
    class Config:
        json_encoders = {
            Decimal: lambda v: format(v, 'e')
        }
        
    @validator('result', pre=True)
    def convert_decimal(cls, value):
        if isinstance(value, (int, float)):
            return Decimal(value)
        return value