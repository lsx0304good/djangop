from rest_framework import serializers

from home.models import AxfWheel, AxfNav, AxfShop, AxfMustbuy, AxfMainshow


class WheelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfWheel
        fields = "__all__"


class NavSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfNav
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfShop
        fields = "__all__"


class MustBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfMustbuy
        fields = "__all__"


class MainShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfMainshow
        fields = "__all__"
