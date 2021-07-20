from rest_framework.permissions import BasePermission

from home.models import AxfUser


class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and isinstance(request.user, AxfUser)