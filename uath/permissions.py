from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.groups.all()[0].name == 'admin_system'
        except:
            return False


class IsPowerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.groups.all()[0].name == 'power_user'
        except:
            return False

