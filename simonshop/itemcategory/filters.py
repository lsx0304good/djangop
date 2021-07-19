from django_filters import rest_framework as filters

from home.models import AxfGoods


class GoodsFilter(filters.FilterSet):
    typeid = filters.CharFilter(field_name="categoryid", lookup_expr="exact")
    childcid = filters.CharFilter(field_name="childcid", method="filter_child_type")
    order_rule = filters.CharFilter(field_name="order_rule", method="get_order_rule")

    class Meta:
        model = AxfGoods
        fields = ['categoryid', 'childcid']

    def filter_child_type(self, queryset, name, value):  # name是字段名，value是传过来的值
        value = int(value)
        if value > 0:  # 有子类
            return queryset.filter(childcid=value)
        else:
            return queryset

    def get_order_rule(self, queryset, name, value):
        value = int(value)
        if value == 0:  # 不排序
            return queryset
        elif value == 1:  # 价格升序
            return queryset.order_by("price")
        elif value == 2:  # 价格降序
            return queryset.order_by("-price")
        elif value == 3:
            return queryset.order_by("productnum")
        elif value == 4:
            return queryset.order_by("-productnum")
