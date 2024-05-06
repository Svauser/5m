import random
import string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer,UserAuthorizationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.
@api_view(['POST'])
def registration(request):
    serializer=UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username=serializer.validated_data.get('username')
    password=serializer.validated_data.get('password')
    confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    User.objects.create_user(username=username,password=password,is_active=False,confirmation_code=confirmation_code)
    return Response(status=status.HTTP_201_CREATED)
@api_view(['POST'])
def authorization(request):
    serializer = UserAuthorizationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user=authenticate(**serializer.validated.data)
    if user:
        # try:
        #     token=Token.objects.get(user=user)
        # except Token.DoesNotExists:
        #     token=Token.objects.create(user=user)
        token,created=Token.objects.get_or_create(user=user)
        return Response(data={'key':token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
def confirm(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    try:
        user = User.objects.get(username=username, confirmation_code=confirmation_code, is_active=False)
        user.is_active = True
        user.save()
        return Response(data={'message': 'User activated successfully.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(data={'error': 'Invalid confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)