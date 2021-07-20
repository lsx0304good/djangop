from django.contrib.auth.hashers import check_password
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from home.models import AxfUser
from myitems.authentications import CustomerAuthentication
from myitems.permissions import CustomerPermission
from myitems.serializers import RegisterInfoSerializer, LoginSerializer
from utils.mytoken import tm


class UserRegisterView(CreateAPIView):
    queryset = AxfUser.objects.all()
    serializer_class = RegisterInfoSerializer

    def create(self, request, *args, **kwargs):
        # 反向序列化
        serializer = RegisterInfoSerializer(data=request.data)

        # 验证
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user_id': user.id})
        return Response({
            'code': 1004,
            'msg': serializer.errors,
            'data': {},
        })


class UserLoginView(CreateAPIView):
    queryset = AxfUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('u_username')
        password = request.data.get('u_password')

        # 查询数据库
        user = AxfUser.objects.filter(u_username=username).first()
        print(user)
        if user and check_password(password, user.u_password):
            # 用用户id做负载
            token = tm.generate_token(user.id)
            return Response({
                'user_id': user.id,
                'token': token,
            })
        return Response({
            'code': 1004,
            'msg': '校验参数失败',
        })


class UserInfoView(ListAPIView):
    queryset = AxfUser.objects.all()
    serializer_class = LoginSerializer
    authentication_classes = (CustomerAuthentication,)
    permission_classes = (CustomerPermission,)

    def get(self, request, *args, **kwargs):
        user = AxfUser.objects.get(pk=request.user.id)
        if user:
            serializer = LoginSerializer(instance=user)
            return Response({"user_info": serializer.data})
        else:
            return Response({"code": 1004, "msg": '用户不存在'})
