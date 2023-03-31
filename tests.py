import pytest
import threading
from decimal import Decimal
from fastapi.testclient import TestClient

from utils import compute_factorial
from main import app

@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as cl:
        yield cl

def test_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.parametrize(
    'input_, expect',
    [
        (1, True),
        (31, True),
        (50, True),
        (10_000, True),
        ('kek', False),
        ('', False)
    ]
)
def test_ws_factorial_straight(client: TestClient, input_, expect):
    with client.websocket_connect("/ws/factorial") as websocket:
        websocket.send_text(input_)
        resp_data = websocket.receive_json()
        assert resp_data.get('code')
        assert (resp_data['code'] == 200) == expect
    
    if expect:
        calc_data = format(compute_factorial(input_), '.2e')
        assert Decimal(calc_data) == Decimal(resp_data['body']['result'])
        
def test_ws_factorial_parallel(client: TestClient):
    sending_data = [
        10_000, 1, 2, 3, 4, 5_000, 50
    ]
    res_data = []
    with client.websocket_connect("/ws/factorial") as websocket:
        for data in sending_data:
            websocket.send_text(data)
        
        resp_data = websocket.receive_json()
        while resp_data:
            res_data.append(int(resp_data['message']))
        
        sending_data.sort()
        
        assert resp_data == sending_data


            
        
        