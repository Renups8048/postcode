import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import pytest
from rest_framework.test import APIClient

import django
django.setup()


@pytest.fixture
def client():
    """Initializing the client"""
    return APIClient()


def test_is_valid_postcode_valid(client):
    """
    Test to check if a valid postcode is identified as valid by the API
    """
    response = client.get('/validate_postcode/', {'postcode': 'EC1A 1BB'})
    assert response.status_code == 200
    assert response.data == "The postcode 'EC1A 1BB' is valid."


def test_is_valid_postcode_invalid(client):
    """
    Test to check if an invalid postcode is identified as invalid by the API
    """
    response = client.get('/validate_postcode/', {'postcode': 'QC1A 1BB1'})
    assert response.status_code == 200
    assert response.data == "The postcode 'QC1A 1BB1' is invalid."


def test_format_postcode_valid(client):
    """
    Test to check if a valid postcode is formatted correctly by the API
    """
    response = client.get('/format_postcode/', {'postcode': 'ec1a1bb'})
    assert response.status_code == 200
    assert response.data == {'formatted_postcode': 'EC1A 1BB'}


def test_format_postcode_invalid(client):
    """
    Test to check if an invalid postcode raises an error by the API
    """
    response = client.get('/format_postcode/', {'postcode': 'EC1A1BBasasas'})
    assert response.status_code == 400
    assert response.data == {'error': 'Invalid postcode'}


def test_validate_postcode_missing_parameter(client):
    """
    Test to check if the API returns an error when the postcode parameter is missing
    """
    response = client.get('/validate_postcode/')
    assert response.status_code == 400
    assert response.data == {'error': 'Postcode parameter missing'}


def test_format_postcode_missing_parameter(client):
    """
    Test to check if the API returns an error when the postcode parameter is missing
    """
    response = client.get('/format_postcode/')
    assert response.status_code == 400
    assert response.data == {'error': 'Postcode parameter missing'}


def test_format_postcode_missing_postcode(client):
    """
    Test to check if the API returns an error when the postcode parameter is not provided
    """
    response = client.get('/format_postcode/', {'not_postcode': ''})
    assert response.status_code == 400
    assert response.data == {'error': 'Postcode parameter missing'}


def test_validate_postcode_missing_postcode(client):
    """
    Test to check if the API returns an error when the postcode parameter is not provided
    """
    response = client.get('/validate_postcode/', {'not_postcode': ''})
    assert response.status_code == 400
    assert response.data == {'error': 'Postcode parameter missing'}