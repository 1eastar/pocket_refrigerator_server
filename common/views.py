from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.conf import settings

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import models, serializers

# Create your views here.

# authentication = TokenAuthentication
# if getattr(settings, 'DEBUG', 'False'):
#     authentication = BasicAuthentication

authentication = BasicAuthentication

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([authentication])
def check_user_auth(request):
    """
    로그인한 상태에서 회원정보 변경 전 인증
    data = {
        password: string,
    }
    response = {
        success: boolean,
        msg: string,
    }
    """
    user = request.user
    input_pw = request.data['password']
    if check_password(input_pw, user.password): 
        return Response({
            'success': 'true',
            'msg': '인증에 성공했습니다'
        }, status=status.HTTP_200_OK)
    return Response({
        'success': 'false',
        'msg': '인증에 실패했습니다'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def signup(request):
    """
    회원가입
    data = {
        email: string,
        pw: string,
        nickname: string,
        gender: number, // 0: man, 1: woman
        birth: string,
        icon: number,
    }
    response = {
        success: boolean,
        msg: string,
        token: string,
        user: object,
    }
    """
    email = request.data['email']
    # user_for_check = User.objects.filter(username=email)
    # if len(user_for_check) > 0:
    #     return Response({
    #         'success': 'false',
    #         'msg': '이미 사용 중인 아이디입니다'
    #     })
    user_for_check = get_object_or_404(User, email=email)
    if len(user_for_check) > 0:
        return Response({
            'success': False,
            'msg': '이미 사용 중인 이메일입니다'
        })

    nickname = request.data['nickname']
    nickname_check = get_object_or_404(models.Userdata, nickname=nickname)
    if len(nickname_check) > 0:
        return Response({
            'success': False,
            'msg': '이미 사용 중인 닉네임입니다'
        })

    pw = request.data['pw']
    gender = request.data['gender']
    birth = request.data['birth']
    icon_id = request.data['icon']

    icon = get_object_or_404(models.Icon, pk=icon_id)
    
    user = User.objects.create_user(username=email, email=email, password=pw)
    # auth.login(request, user)      # 무슨 역할? 백엔드 내부 역할?
    token = Token.objects.get(user=request.user).key
    userdata = models.Userdata.create(nickname=nickname, gender=gender, birth=birth, user=user, icon=icon)
    
# userdata serializer를 authserializer에 넣어야 댐
    serializer = serializers.AuthSerializer(user)
    return Response({
        'success': True,
        'msg': '회원가입에 성공하였습니다',
        'token': token,
        'user': serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def signin(request):
    """
    로그인
    data = {
        user_id: string,
        user_pw: string
    }
    response = {
        success: boolean,
        msg: string,
        token: string,
        user: object,
    }
    """
    user_id = request.data['user_id']
    user_pw = request.data['user_pw']
    user_unchecked = User.objects.get(username=user_id)
    if user_unchecked is None:
        return Response({
            'success': 'false',
            'msg': '존재하지 않는 아이디입니다'
        }, status=status.HTTP_400_BAD_REQUEST)
    if check_password(user_unchecked, user_pw):
        user_checked = user_unchecked
        token = Token.objects.get(user=user_checked)
        serializer = serializers.AuthSerializer(user_checked)
        return Response({
            'success': 'false',
            'msg': '로그인 되었습니다.',
            'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
        'success': 'false',
        'msg': '비밀번호가 틀렸습니다'
    }, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        get user info
        """
        if self.request.user.is_authenticated:
            user = request.user
            serializer = serializers.AuthSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': 'false',
                'msg': '로그인을 먼저 해주세요.'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, format=None):
        """
        update userdata
        data = {
            nickname?: string
            main_honor?: number,
        }
        """
        user = request.user
        userdata = models.Userdata.objects.get(user=user)
        new_nickname = request.data['nickname']
        new_main_honor = request.data['main_honor']
        if new_nickname is not None:
            userdata.nickname = new_nickname
            userdata.save()
        if new_main_honor is not None:
            new_honor = models.Honor.objects.get(id=new_main_honor)
            userdata.main_honor = new_honor
            userdata.save()
        serializer = serializers.UserdataSerializer(userdata)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AuthInView(APIView):
    authentication_classes = [authentication]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """

        """


class NoticeViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication]
    permission_classes = [AllowAny]

    queryset = models.Notice.objects.order_by('-updated_at')
    serializer_class = serializers.NoticeSerializer

    def perform_create(self, serializer):
        # serializer.save()
        return super().perform_create(serializer)


class BarcodeViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    queryset = models.Barcode.objects.all()
    serializer_class = serializers.BarcodeSerializer



@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([authentication])
def barcode_data(request):
    """
    data = {
        barcode: string,
    }
    """
    barcode = request.GET.get('barcode')
    return Response({}, status=status.HTTP_200_OK)