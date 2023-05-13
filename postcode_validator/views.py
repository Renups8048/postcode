import re
from rest_framework.decorators import api_view
from rest_framework.response import Response

def is_valid_postcode(postcode):
    pattern = r"^[A-Z]{1,2}[0-9R][0-9A-Z]?[ ]?[0-9][A-Z]{2}$"
    return bool(re.match(pattern, postcode.upper().replace(" ", "")))

@api_view(['GET'])
def validate_postcode(request):
    postcode = request.GET.get('postcode')
    if not postcode:
        return Response({'error': 'Postcode parameter missing'})
    is_valid = is_valid_postcode(postcode)
    return Response({'valid': is_valid})

@api_view(['GET'])
def format_postcode(request):
    postcode = request.GET.get('postcode')
    if not postcode:
        return Response({'error': 'Postcode parameter missing'})
    is_valid = is_valid_postcode(postcode)
    if is_valid:
        formatted_postcode = f"{postcode[:-3]} {postcode[-3:]}"
        return Response({'formatted_postcode': formatted_postcode.upper()})
    else:
        return Response({'error': 'Invalid postcode'})
