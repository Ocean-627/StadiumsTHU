from rest_framework.permissions import BasePermission


class UserPermission(object):
    message = "You are on the blacklist. Therefore this request is forbidden."

    def has_permission(self, request, view):
        # allow GET method
        if request.method == 'GET':
            return True
        user = request.user
        if user.inBlacklist:
            return False
        else:
            return True
