from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from home.models import AxfCart
from myitems.authentications import CustomerAuthentication
from myitems.permissions import CustomerPermission
from shoppingcart.serializers import CartAddSerializer, CartSerializer


class CartAddView(CreateAPIView):
    queryset = AxfCart.objects.all()
    serializer_class = CartAddSerializer
    authentication_classes = (CustomerAuthentication,)
    permission_classes = (CustomerPermission,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            gid = serializer.data.get("goodsid", 0)

            # 查询购物车中是否存在商品id等于gid的
            record = AxfCart.objects.filter(c_user=request.user, c_goods_id=int(gid))
            if record:  # 记录存在，则数量加一
                record = record[0]
                record.c_goods_num += 1
            else:
                # 如果不存在，则添加新的对象
                record = AxfCart()
                record.c_goods_id = int(gid)
                record.c_user = request.user
                record.c_goods_num = 1
            record.save()
            return Response({'c_goods_num': record.c_goods_num})


class CartSubView(CreateAPIView):
    queryset = AxfCart.objects.all()
    serializer_class = CartAddSerializer
    authentication_classes = (CustomerAuthentication,)
    permission_classes = (CustomerPermission,)

    def create(self, request, *args, **kwargs):
        gid = int(request.data.get("goodsid", 0))
        # 查询登录用户选中的商品
        record = AxfCart.objects.filter(c_user=request.user, c_goods_id=gid).first()
        num = 0
        if record:
            if record.c_goods_num > 1:
                record.c_goods_num -= 1  # 商品数量减一
                num = record.c_goods_num
                record.save()
            else:
                record.delete()  # 数量为0，删除购物车中商品
            return Response({"c_goods_num": num})


class CartShowView(ListAPIView):
    queryset = AxfCart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = (CustomerAuthentication,)
    permission_classes = (CustomerPermission,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 过滤当前用户的购物车数据
        queryset = queryset.filter(c_user=request.user)
        serializer = CartSerializer(instance=queryset, many=True)
        goods = AxfCart.objects.filter(c_user=request.user, c_is_select=True)
        total = sum([rec.c_goods_num * rec.c_goods.price for rec in goods])

        is_all_select = len(queryset) == len(goods)
        print(serializer.data)
        return Response({
            "title": "购物车",
            "is_all_select": is_all_select,
            "total_price": str(total),
            "carts": serializer.data
        })


class CartCancelView(APIView):
    authentication_classes = (CustomerAuthentication,)
    permission_classes = (CustomerPermission,)

    def patch(self, request, pk):
        print(pk)
        record = AxfCart.objects.filter(c_user=request.user, pk=pk).first()
        if record:
            # 和原来进行相反操作
            record.c_is_select = not record.c_is_select
            record.save()
            return Response({})
        return Response({'code': 107, 'msg': '请求失败'})
