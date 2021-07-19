from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from home.models import AxfGoods, AxfWheel, AxfNav, AxfShop, AxfMainshow, AxfMustbuy
from home.serializers import WheelSerializer, NavSerializer, ShopSerializer, MainShowSerializer, MustBuySerializer


class HomeView(GenericAPIView):
    # queryset = AxfWheel.objects.all()
    # serializer_class = WheelSerializer

    def get(self, request, *args, **kwargs):
        wheel = WheelSerializer(instance=AxfWheel.objects.all(), many=True)
        nav = NavSerializer(instance=AxfNav.objects.all(), many=True)
        shop = ShopSerializer(instance=AxfShop.objects.all(), many=True)
        mainshow = MainShowSerializer(instance=AxfMainshow.objects.all(), many=True)
        mustbuy = MustBuySerializer(instance=AxfMustbuy.objects.all(), many=True)

        # return Response({
        #     'code': 200,
        #     'msg': "请求成功",
        #     'data': {
        #         'main_wheels': wheel.data,
        #         'main_navs': nav.data,
        #         'main_shops': shop.data,
        #         'main_shows': mainshow.data,
        #         'main_mustbuys': mustbuy.data,
        #     }
        # })

        return Response({
            'main_wheels': wheel.data,
            'main_navs': nav.data,
            'main_shops': shop.data,
            'main_shows': mainshow.data,
            'main_mustbuys': mustbuy.data,
        })
