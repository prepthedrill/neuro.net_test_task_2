import json

import pytest
import requests
from flask import Flask

from ..distance_calc import distance_calc


@pytest.fixture
def app():
    """
    Фикстура для создания экземпляра Flask-приложения
    с зарегистрированным Blueprint.
    """
    app = Flask(__name__)
    app.register_blueprint(distance_calc)
    yield app


@pytest.fixture
def client(app):
    """
    Фикстура для создания клиента тестирования Flask-приложения.
    """
    return app.test_client()


def test_valid_address_inside_MKAD(client):
    """
    Тест: запрос с валидным адресом внутри МКАД.
    """
    address = "Садовая-Кудринская улица, 1, Москва"
    response = client.post('/distance-calc', json={'address': address})
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['adress_inside_MKAD'] == 1


def test_valid_address_outside_MKAD(client):
    """
    Тест: запрос с валидным адресом снаружи МКАД.
    """
    address = "Театральная площадь, 1, Калуга"
    response = client.post('/distance-calc', json={'address': address})
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['adress_inside_MKAD'] == 0
    assert 'distance' in data


def test_invalid_address(client):
    """
    Тест: запрос с невалидным адресом.
    """
    address = "INVALID ADRESS 100"
    response = client.post('/distance-calc', json={'address': address})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'error' in data
    assert "Couldn't find such address in Yandex API" in data['error']


def test_calc_distance(client):
    """
    Тест проверят правильность расчета расстояния от адресса до МКАДа.
    """
    address = "Театральная площадь, 1, Калуга"
    response = client.post('/distance-calc', json={'address': address})
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['adress_inside_MKAD'] == 0
    assert 'distance' in data
    assert data['distance'] == '144.249'


def test_missing_address_field(client):
    """
    Тест: запрос с отсутствующим полем 'address'
    """
    response = client.post('/distance-calc', json={})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'error' in data
    assert "The address field was not found" in data['error']


def test_yandex_api_unavailable(client, monkeypatch):
    """
    Тест на то, что API Яндекса недоступна.
    """
    def mock_requests_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Mocked Request Exception")

    monkeypatch.setattr(requests, 'get', mock_requests_get)

    address = "Садовая-Кудринская улица, 1, Москва"
    response = client.post('/distance-calc', json={'address': address})
    data = json.loads(response.data)

    assert response.status_code == 500
    assert 'error' in data
    assert "The Yandex API is unavailable" in data['error']
