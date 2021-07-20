from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from home.models import AxfFoodtype, AxfGoods
from itemcategory.filters import GoodsFilter
from itemcategory.serializers import FoodtypeSerializer, GoodsSerializer


class FoodTypeView(ListAPIView):
    queryset = AxfFoodtype.objects.all()
    serializer_class = FoodtypeSerializer


# 因为需要过滤，所以继承generic
class GoodListView(GenericAPIView):
    queryset = AxfGoods.objects.all()
    serializer_class = GoodsSerializer
    filter_class = GoodsFilter

    def get(self, request, *args, **kwargs):
        typeid = request.query_params.get("typeid")
        childcid = request.query_params.get("childcid")

        # 使用自定义过滤类过滤结果集
        queryset = self.filter_queryset(self.get_queryset())
        # 序列化
        serializer = GoodsSerializer(instance=queryset, many=True)

        childtypes = AxfFoodtype.objects.filter(typeid=int(typeid)).first()
        order_rule_list = [{'order_name': '综合排序', 'order_value': 0}, {'order_name': '价格升序', 'order_value': 1}, {'order_name': '价格降序', 'order_value': 2}, {'order_name': '销量升序', 'order_value': 3}, {'order_name': '销量降序', 'order_value': 4}]
        return Response({
            "goods_list": serializer.data,
            'order_rule_list': order_rule_list,
            'foodtype_childname_list': childtypes.childtypes,
        })


