from rest_framework.permissions import BasePermission
class Mypression(BasePermission):
    message = '你没有此权限'
    def has_permission(self,request,view):
        # print(request.user)
        # print(request.user.user_type)
        if request.user.user_type != 3:
            return False
        return True