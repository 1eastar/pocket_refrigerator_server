from django.shortcuts import render, redirect, get_object_or_404
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
from rest_framework.throttling import UserRateThrottle
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import models, serializers
from recipe.models import Recipe, Comment

# Create your views here.

class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'


authentication = TokenAuthentication
if getattr(settings, 'DEBUG', 'False'):
    authentication = BasicAuthentication

# authentication = BasicAuthentication

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
            'success': True,
            'msg': '인증에 성공했습니다'
        }, status=status.HTTP_200_OK)
    return Response({
        'success': False,
        'msg': '인증에 실패했습니다'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def verify(request):
    """
    data = {
        email: string,
    }
    """
    email = request.data['email']
    user_for_check = models.User.objects.filter(email=email)
    if len(user_for_check) > 0:
        return Response({
            'success': False,
            'msg': '이미 사용 중인 이메일입니다.'
        })
    return Response({
        "success": True,
        "msg": "사용 가능한 이메일입니다."
    })


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def signup(request):
    """
    회원가입
    data = {
        email: string,
        pw: string,
        gender: number, // 0: man, 1: woman
        birth: string,
        icon: number,
        nickname: string,
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

    nickname = request.data['nickname']
    # nickname_check = models.Userdata.objects.filter(nickname=nickname)
    nickname_check = models.User.objects.filter(nickname=nickname)
    if len(nickname_check) > 0:
        return Response({
            'success': False,
            'msg': '이미 사용 중인 닉네임입니다'
        })
    
    pw = request.data['pw']
    gender = request.data['gender']
    birth = request.data['birth']
    icon_id = request.data['icon']
    icon = get_object_or_404(models.Icon, id=icon_id)
    user = models.User.objects.create_user(
        email=email,
        password=pw,
        nickname=nickname,
        gender=gender,
        birth=birth,
        user=user,
        icon=icon
    )
    # auth.login(request, user) 
    token = get_object_or_404(Token, user=user).key

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
    user_unchecked = auth.authenticate(email=user_id, password=user_pw)

    if user_unchecked is None:
        return Response({
            'success': False,
            'msg': '이메일 또는 비밀번호를 확인해주세요'
        }, status=status.HTTP_400_BAD_REQUEST)

    if user_unchecked.check_password(user_pw):
        user_checked = user_unchecked
        token = get_object_or_404(Token, user=user_checked)
        serializer = serializers.AuthSerializer(user_unchecked)
        return Response({
            'success': True,
            'msg': '로그인 되었습니다.',
            'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
        'success': False,
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
    
    def patch(self, request, format=None):
        """
        update userdata
        data = {
            nickname?: string
            birth?: string // ex)1998
            gender?: number // 0: man, 1:woman
            // main_honor?: number, // 일단 생략
        }
        """
        user = self.request.user
        serializer = serializers.AuthSerializer(user, data=request.data, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        user = self.request.user
        user.delete()
        return Response({
            "success": True,
            "msg" : '성공적으로 탈퇴했습니다.'
        })

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
@permission_classes([AllowAny])
@authentication_classes([])
def get_barcode_data(request):
    """
    data = {
        barcode: string,
    }
    """
    barcode = request.GET.get('barcode')
    food_data = get_object_or_404(models.Food, BAR_CD=barcode)
    serializer = serializers.FoodSerializer(food_data)
    return Response({
        'success': True,
        'msg': '데이터 불러오기에 성공했습니다.',
        'food': serializer.data
    }, status=status.HTTP_200_OK)

######### DB에 없는 바코드 정보 저장 api ###########
############# 악용 우려가 있어 보류 ###############
# @api_view(http_method_names=['POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([authentication])
# def set_barcode_data(request):
#     """
#     data = {
#         BAR_CD: string,
#         PRDLST_DCNM?: string,
#         PRDLST_NM?: string,
#         BSSH_NM?: string,
#         PRMS_DT?: string,
#         CLSBIZ_DT?: string,
#         INDUTY_NM?: string,
#         SITE_ADDR?: string,
#         POG_DAYCNT?: string,
#         END_DT?: string,
#         PRDLST_REPORT_NO?: string,
#     }
#     """
    
#     return Response({
#         'success': True,
#         'msg': '데이터를 저장했습니다.',
#         'food': serializer.data
#     }, status=status.HTTP_200_OK)


# class ReportView(APIView):
#     authentication_classes = [authentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):

#         return

@api_view(http_method_names=['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def report(request):
    """
    data = {
        author_id: number,
        report_type: number,
        report_category: number,
        content: string,

        user_id?: number,
        recipe_id?: number,
        comment_id?: number,
    }
    """
    author_id = request.GET['author_id']
    report_type = int(request.GET['repot_type'])
    report_category = request.GET['report_category']
    content = request.GET['content']
    print(author_id, report_type, report_category, content)
    if report_type == 0:
        user = get_object_or_404(models.User, pk=request.GET['user_id'])
        report = models.Report.objects.create(
            author_id=author_id,
            report_type=report_type,
            report_category=report_category,
            content=content,
            user=user
        )
        user.report_num += 1
        user.save()
        serializer = serializers.ReportSerializer(report)
        return Response({
            'success': True,
            'msg': '해당 유저를 신고하였습니다',
            'report': serializer.data,
        }, status=status.HTTP_200_OK)
    if report_type == 1:
        recipe = get_object_or_404(Recipe, pk=request.GET['recipe_id'])
        recipe.report_num += 1
        recipe.save()
        report = models.Report.objects.create(
            author_id=author_id,
            report_type=report_type,
            report_category=report_category,
            content=content,
            recipe=recipe
        )
        serializer = serializers.ReportSerializer(report)
        return Response({
            'success': True,
            'msg': '해당 레시피를 신고하였습니다',
            'report': serializer.data,
        }, status=status.HTTP_200_OK)
    if report_type == 2:
        comment = get_object_or_404(Comment, pk=request.GET['comment_id'])
        comment.report_num += 1
        comment.save()
        report = models.Report.objects.create(
            author_id=author_id,
            report_type=report_type,
            report_category=report_category,
            content=content,
            comment=comment
        )
        serializer = serializers.ReportSerializer(report)
        return Response({
            'success': True,
            'msg': '해당 댓글을 신고하였습니다',
            'report': serializer.data,
        }, status=status.HTTP_200_OK)