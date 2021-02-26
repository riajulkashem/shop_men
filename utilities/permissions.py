from rest_framework import permissions as perm
from utilities.methods import permitted, check_permitted
from utilities.variables import MASTER_ADMIN, ADMIN, SUPER_ADMIN

SAFE_METHODS = ('HEAD', 'OPTIONS')


class IsMaster(perm.BasePermission):
    """
    On every request check user has permission
    to add change remove with it's method
    Example: if request.user.has_permission(add_obeject)
     and method == POST: return True
    """
    message: str

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return str(request.user.role.name) in [MASTER_ADMIN, SUPER_ADMIN]

    def has_object_permission(self, request, view, obj):
        return check_permitted(request, obj, self)


#     TODO Uncomment this


class IsAdmin(perm.BasePermission):
    message: str

    def has_permission(self, request, view):
        if not hasattr(request.user, 'institute') or \
                not permitted(request, 'view', view.queryset.model, self):
            return False
        return request.user.role.name == ADMIN

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if hasattr(obj, 'institute'):
            return obj.institute == request.user.institute and \
                   check_permitted(request, obj, self)
        return check_permitted(request, obj, self)


class IsAdminForm(perm.BasePermission):
    message: str

    def has_permission(self, request, view):
        if not hasattr(request.user, 'institute'):
            return False
        return request.user.role.name == ADMIN


class AdminOrMasterAdmin(perm.BasePermission):

    def has_permission(self, request, view):
        if request.user.role.name in [ADMIN, MASTER_ADMIN, SUPER_ADMIN]:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return check_permitted(request, obj, self)


class AdminOnly(perm.BasePermission):

    def has_permission(self, request, view):
        return request.user.role.name == ADMIN and hasattr(request.user, 'institute')

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return check_permitted(request, obj, self)


class ReadOnlyExceptMasterAdmin(perm.BasePermission):

    def has_permission(self, request, view):
        if request.user.role.name == ADMIN and hasattr(
                request.user, 'institute'
        ):
            return True
        return request.user.role.name in [MASTER_ADMIN, SUPER_ADMIN]

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return check_permitted(request, obj, self)
