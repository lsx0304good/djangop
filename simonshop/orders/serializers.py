from rest_framework import serializers

from home.models import AxfOrder, AxfOrdergoods
from itemcategory.serializers import GoodsSerializer


class OrderGoodsSerializer(serializers.ModelSerializer):
    # 关联信息，在订单里显示详细商品信息！
    o_goods = GoodsSerializer()

    class Meta:
        model = AxfOrdergoods
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfOrder
        fields = "__all__"

    # 修改序列化结果
    def to_representation(self, instance):
        # 调用父类方法获取序列化后的数据，instance是订单对象
        data = super().to_representation(instance)
        orderGoods = instance.goods.all()  # 反向查找
        serializer = OrderGoodsSerializer(instance=orderGoods, many=True)
        data["order_goods_info"] = serializer.data
        print(data)
        return data
