import uuid
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import ItemSerializer, OrderSerializer, OrderCreateSerializer
from .models import Order, Item
from customers.models import Customer
from access_control.user_permissions import (
    AdminAccessPermission,
    CashierAccessPermission,
    CustomerAccessPermission,
)


class ItemViewSet(viewsets.ViewSet):
    # for browsable api update/create view
    serializer_class = ItemSerializer

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
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise e

    def create(self, request):
        try:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e

    def retrieve(self, request, pk=None):
        try:
            queryset = Item.objects.all()
            item = get_object_or_404(queryset, pk=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except Exception as e:
            raise e

    def update(self, request, pk=None):
        try:
            queryset = Item.objects.all()
            item = get_object_or_404(queryset, pk=pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e

    def partial_update(self, request, pk=None):
        try:
            queryset = Item.objects.all()
            item = get_object_or_404(queryset, pk=pk)
            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e

    def destroy(self, request, pk=None):
        try:
            print("ready to del", pk)
            queryset = Item.objects.all()
            item = get_object_or_404(queryset, pk=pk)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise e


class OrderViewSet(viewsets.ViewSet):
    serializer_class = OrderSerializer
    # def get_permissions(self):
    #     if self.action in ['create', 'update','partial_update' ,'destroy']:
    #         permission_classes = [AdminAccessPermission]
    #     else:
    #         permission_classes = [AdminAccessPermission|CashierAccessPermission|CustomerAccessPermission]
    #     return [permission() for permission in permission_classes]

    def list(self, request):
        filter = {}
        filter["customer_id"] = request.user.id
        if request.query_params.get("cust_id") is not None:
            filter["customer_id"] = request.query_params.get("cust_id")
        try:
            orders = Order.objects.filter(**filter)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise e

    def create(self, request):
        try:
            serializer = OrderCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e

    def retrieve(self, request, pk=None):
        try:
            queryset = Order.objects.all()
            order = get_object_or_404(queryset, pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Exception as e:
            raise e

    def update(self, request, pk=None):
        try:
            queryset = Order.objects.all()
            order = get_object_or_404(queryset, pk=pk)
            serializer = OrderCreateSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e

    def partial_update(self, request, pk=None):
        try:
            queryset = Order.objects.filter()
            order = get_object_or_404(queryset, pk=pk)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e

    def destroy(self, request, pk=None):
        try:
            queryset = Order.objects.filter()
            order = get_object_or_404(queryset, pk=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise e