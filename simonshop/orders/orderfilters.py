from django_filters import rest_framework as filters

from home.models import AxfOrder
from simonshop.settings import ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_SEND


class OrderFilter(filters.FilterSet):
    o_status = filters.CharFilter(field_name="o_status", method="filter_by_status")
    class Meta:
        model = AxfOrder
        fields = ["o_status"]

    def filter_by_status(self, queryset, name, value):
        print(value, name)
        if value == "not_pay":  # 未付款
            return queryset.filter(o_status=ORDER_STATUS_NOT_PAY)
        elif value == "not_send":
            return queryset.filter(o_status=ORDER_STATUS_NOT_SEND)
        return queryset