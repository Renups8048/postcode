import os
import pytest
from django.conf import settings
from django.test import RequestFactory

os.environ['DJANGO_SETTINGS_MODULE'] = 'postcode.settings'
settings.configure()

from .views import is_valid_postcode, format_postcode

# Valid postcodes
valid_postcodes = [
    ("EC1A 1BB", True),
    ("EC1A1BB", True),
    ("ec1a1bb", True),
    ("w1a0ax", True),
    ("m11ae", True),
    ("b338th", True),
    ("cr26xh", True),
    ("dn551pt", True),
    ("BL01AA", True),
]

# Invalid postcodes
invalid_postcodes = [
    ("QC1A 1BB", False),
    ("VC1A 1BB", False),
    ("XC1A 1BB", False),
    ("AI1A 1BB", False),
    ("AJ1A 1BB", False),
    ("A9X 0AX", False),
]


@pytest.mark.parametrize("postcode, expected_result", valid_postcodes)
def test_is_valid_postcode_valid(postcode, expected_result):
    assert is_valid_postcode(postcode) == expected_result


@pytest.mark.parametrize("postcode, expected_result", invalid_postcodes)
def test_is_valid_postcode_invalid(postcode, expected_result):
    assert is_valid_postcode(postcode) == expected_result


def test_format_postcode_valid():
    factory = RequestFactory()
    request = factory.get('/validate_postcode')
    response = format_postcode(request, "ec1a1bb")
    assert response.status_code == 200
    assert response.data == {'formatted_postcode': 'EC1A 1BB'}

def test_format_postcode_invalid():
    factory = RequestFactory()
    request = factory.get('/validate_postcode')
    response = format_postcode(request, "EC1A1BBasasas")
    assert response.status_code == 400
    assert response.data == {'error': 'Invalid postcode'}
