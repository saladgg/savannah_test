import json
from django.contrib.auth.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import Permission

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from customers.models import Customer,UserAccessGroup

class TokenSerializer(TokenObtainPairSerializer):
    def adminPerms(self):
        admin_group_id = Group.objects.get(name='admin_access').id
        perms=Permission.objects.filter(group__id=admin_group_id).values_list('codename', flat=True)
        admin_perms = json.dumps(list(perms), cls=DjangoJSONEncoder)
        return admin_perms

    def userPerms(self,staff_user):
        group_ids = UserAccessGroup.objects.filter(user_id=staff_user.id).values_list('group__id',flat=True)
        user_permissions = Permission.objects.filter(group__id__in=group_ids).values_list('codename',flat=True)
        user_perms = json.dumps(list(user_permissions), cls=DjangoJSONEncoder)
        if len(user_perms)>1:
            return user_perms
        else:
            return []
    
    @classmethod
    def get_token(self, user):
        token = super().get_token(user)
        try:
            access_groups = UserAccessGroup.objects.filter(user_id=user.id).values_list('group__name',flat=True)
            if 'admin_access' in access_groups:
                token['permissions'] = self.adminPerms(self)
                return token
            elif not 'admin_access' in access_groups:
                sys_user = Customer.objects.filter(email=user.email,is_active=True).first()
                if sys_user:
                    token['permissions'] = self.userPerms(self,sys_user)
                    return token
                else:
                    raise PermissionDenied
            else:
                raise PermissionDenied
        except Exception as e:
            raise e
          
class CustomTokenView(TokenObtainPairView):
    serializer_class = TokenSerializer

