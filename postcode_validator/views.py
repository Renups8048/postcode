"""Main logic of postcode validator and formatter API's"""
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def is_valid_postcode(postcode):
    """Check the postcode is valid or not"""
    pattern = r"^[A-Z]{1,2}[0-9R][0-9A-Z]?[ ]?[0-9][A-Z]{1,2}$"
    return bool(re.match(pattern, postcode.upper().replace(" ", "")))


@api_view(['GET'])
def validate_postcode(request):
    """validation API"""
    postcode = request.GET.get('postcode')
    if not postcode:
        return Response({'error': 'Postcode parameter missing'}, status=status.HTTP_400_BAD_REQUEST)
    is_valid = is_valid_postcode(postcode)
    if is_valid:
        return Response(f"The postcode '{postcode}' is valid.")
    return Response(f"The postcode '{postcode}' is invalid.")


@api_view(['GET'])
def format_postcode(request):
    """Validate and formatting process"""
    postcode = request.GET.get('postcode')
    if not postcode:
        return Response({'error': 'Postcode parameter missing'}, status=status.HTTP_400_BAD_REQUEST)
    is_valid = is_valid_postcode(postcode)
    if is_valid:
        formatted_postcode = f"{postcode[:-3]} {postcode[-3:]}"
        return Response({'formatted_postcode': formatted_postcode.upper()})
    return Response({'error': 'Invalid postcode'}, status=status.HTTP_400_BAD_REQUEST)
