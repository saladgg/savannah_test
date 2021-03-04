import random, uuid, string, time
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import CustomerSerializer, CreateCustomerSerializer
from .models import Customer
from customers.user_permissions import (
    AdminAccessPermission,
    CashierAccessPermission,
    CustomerAccessPermission,
)


def getCode():
    ms = int(time.time() * 1000.0)
    rand_1 = "".join(
        random.choices(string.ascii_uppercase + string.digits + str(ms), k=9)
    )
    return rand_1


class CustomerViewSet(viewsets.ViewSet):
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [AdminAccessPermission]
        else:
            permission_classes = [
                AdminAccessPermission
                | CashierAccessPermission
                | CustomerAccessPermission
            ]
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise e

    def create(self, request):
        try:
            serializer = CreateCustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(code=getCode())
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e

    def retrieve(self, request, pk=None):
        try:
            queryset = Customer.objects.all()
            customer = get_object_or_404(queryset, pk=pk)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Exception as e:
            raise e

    def update(self, request, pk=None):
        try:
            queryset = Customer.objects.all()
            customer = get_object_or_404(queryset, pk=pk)
            serializer = CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e

    def partial_update(self, request, pk=None):
        try:
            queryset = Customer.objects.all()
            customer = get_object_or_404(queryset, pk=pk)
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e

    def destroy(self, request, pk=None):
        try:
            queryset = Customer.objects.all()
            customer = get_object_or_404(queryset, pk=pk)
            customer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise e
