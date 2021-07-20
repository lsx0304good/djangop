from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from home.models import AxfOrder, AxfCart, AxfOrdergoods
from myitems.authentications import CustomerAuthentication
from myitems.permissions import CustomerPermission
from orders.orderfilters import OrderFilter
from orders.serializers import OrderSerializer


class OrdersView(ListCreateAPIView):
    queryset = AxfOrder.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (CustomerAuthentication,)
    permission_classes = (CustomerPermission,)
    filter_class = OrderFilter

    # 生成订单
    def create(self, request, *args, **kwargs):
        carts = AxfCart.objects.filter(c_user=request.user, c_is_select=True)
        theOrder = AxfOrder()
        theOrder.o_price = sum([rec.c_goods_num * rec.c_goods.price for rec in carts])
        theOrder.o_user = request.user
        theOrder.save()

        # 维护订单
        for obj in carts:
            # 商品记录
            detail = AxfOrdergoods()
            detail.o_order = theOrder  # 订单
            detail.o_goods = obj.c_goods  # 产品
            detail.o_goods_num = obj.c_goods_num  # 商品数量
            detail.save()

            # 清空购物车中的obj
            obj.delete()
        return Response({
            'order_id': theOrder.id
        })

    # 查询订单
    def list(self, request, *args, **kwargs):
        # 找出登录用户的订单
        theOrders = AxfOrder.objects.filter(o_user=request.user)
        theOrders = self.filter_queryset(theOrders)
        serializer = OrderSerializer(instance=theOrders, many=True)
        return Response(serializer.data)
