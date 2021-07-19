from rest_framework import serializers

from home.models import AxfFoodtype, AxfGoods


class FoodtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfFoodtype
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfGoods
        fields = '__all__'
