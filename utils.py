import json
from decimal import Decimal

def compute_factorial(n: int) -> int:
    result = 1
    for i in range(1, n+1):
        result *= i
    
    return result

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return f'{o:.2e}' if o > 1e6 else f'{o:.0f}'
        
        return super().default(o)
