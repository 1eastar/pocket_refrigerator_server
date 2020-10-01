from django.shortcuts import render, get_object_or_404
from django.conf import settings

from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

authentication = TokenAuthentication
if getattr(settings, 'DEBUG', 'False'):
    authentication = BasicAuthentication

@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([authentication])
def getAuthToken(request):
    user = request.user
    token = get_object_or_404(Token, user=user)
    return Response({
        "success": True,
        "token": token.key,
    })