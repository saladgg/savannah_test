from rest_framework import serializers
from customers.models import Customer
from .models import Order, Item


class CustomerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = (
            "added_on",
            "updated_on",
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    # customer = serializers.IntegerField()
    # item = serializers.IntegerField()
    class Meta:
        model = Order
        exclude = (
            "added_on",
            "updated_on",
        )


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    item = ItemSerializer()

    class Meta:
        model = Order
        exclude = (
            "added_on",
            "updated_on",
        )
