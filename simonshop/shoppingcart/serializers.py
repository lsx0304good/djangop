from rest_framework import serializers

from home.models import AxfGoods, AxfCart


class CartAddSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    goodsid = serializers.IntegerField(required=True)


# 商品序列化
class AxfGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfGoods
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    # 关联序列化，c_goods必须是模型字段名
    c_goods = AxfGoodsSerializer()
    class Meta:
        model = AxfCart
        fields = "__all__"
