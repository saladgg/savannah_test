from rest_framework import permissions
from customers.models import UserAccessGroup

class AdminAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        access_groups = UserAccessGroup.objects.filter(user_id=request.user.id).values_list('group__name',flat=True)
        if 'admin_access' in access_groups:
            return True
        else:
            return False
    
class CashierAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        access_groups = UserAccessGroup.objects.filter(user_id=request.user.id).values_list('group__name',flat=True)
        if 'cashier_access' in access_groups:
            return True
        else:
            return False

class CustomerAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        access_groups = UserAccessGroup.objects.filter(user_id=request.user.id).values_list('group__name',flat=True)
        if 'customer_access' in access_groups:
            return True
        else:
            return False

