import pytest
from decimal import Decimal
import threading
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
        factorial = Decimal(compute_factorial(input_))
        calc_data = format(factorial, '.2e')
        assert Decimal(calc_data) == Decimal(resp_data['body']['result'])
        
def test_ws_factorial_parallel(client: TestClient):
    # 50_000 должно дольше всего обрабатываться, так что в результате будет не первый в списке
    sending_data = [
        50_000, 1, 2, 3, 4, 5_00, 50
    ]
    res_data = []
    with client.websocket_connect("/ws/factorial") as websocket:
        for data in sending_data:
            websocket.send_text(data)
        
        resp_data = websocket.receive_json()
        for _ in range(len(sending_data) - 1):
            res_data.append(int(resp_data['message']))
            resp_data = websocket.receive_json()
            
            assert resp_data['code'] == 200
        
        sending_data.sort()
        print(res_data)
        
        assert res_data != sending_data

def test_ws_factorial_multiple_clients():
    datas = [10_000 + i for i in range(20)]
    
    def __sending_requests(client):
        sended = set()
        received = set()
        
        with client.websocket_connect("/ws/factorial") as websocket:
            for _ in range(10):
                if not datas: break
                to_send = datas.pop()
                sended.add(to_send)
                
                websocket.send_text(to_send)
            
            for _ in range(len(sended)):
                resp = websocket.receive_json()
                
                assert resp['code'] == 200
                
                received.add(
                    int(resp['message'])
                )
            
            assert sended == received
        
    tasks = []    
    for _ in range(2):
        t = threading.Thread(target=__sending_requests, args=(TestClient(app), ))
        t.start()
        tasks.append(t)
    
    for t in tasks:
        t.join()
        
    
    
    

            
        
        