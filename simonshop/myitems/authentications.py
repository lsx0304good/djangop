from rest_framework.authentication import BaseAuthentication

from home.models import AxfUser
from utils.mytoken import tm


class CustomerAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 获取token，可能是GET传参(问号传参)，也可能是POST传参获取token
        token = request.query_params.get("token") or request.data.get("token")
        if token:
            try:
                uid = tm.confirm_token(token)
                print("authorized:", uid)
                user = AxfUser()
                user.id = uid
                return user, None
            except:
                return None
        else:
            return None
