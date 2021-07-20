from django.contrib.auth.hashers import make_password
from rest_framework import serializers

# 不能用Model Serializer，因为一些信息如 确认密码 在模型里没有
from home.models import AxfUser


class RegisterInfoSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True)
    u_password = serializers.CharField(min_length=3, error_messages={
        "min_length": "密码长度不能小于3位",
    })
    u_password2 = serializers.CharField(min_length=3, error_messages={
        "min_length": "密码长度不能小于3位",
    })
    u_email = serializers.EmailField(required=True)

    # 用户名唯一
    def validate_u_username(self, value):
        print(value)
        # 查询数据库
        user = AxfUser.objects.filter(u_username=value)
        if user:
            raise serializers.ValidationError("用户名已存在")
        return value

    # 邮箱验证
    def validate_u_email(self, value):
        user = AxfUser.objects.filter(u_email=value)
        if user:
            raise serializers.ValidationError("邮箱重复")
        return value

    # 全局验证
    def validate(self, attrs):
        password = attrs.get("u_password")
        password2 = attrs.get("u_password2")
        if password2 != password:
            raise serializers.ValidationError("两次密码不一致")
        return attrs

    # 需要重写 create 方法
    def create(self, validated_data):
        new_user = AxfUser()
        new_user.u_username = validated_data.get('u_username')
        new_user.u_password = make_password(validated_data.get('u_password'))
        new_user.u_email = validated_data.get('u_email')
        new_user.is_active = 1
        new_user.is_delete = 0
        new_user.save()
        return new_user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfUser
        fields = "__all__"
