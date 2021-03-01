from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIRequestFactory, APITestCase
from unittest import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from django.contrib.auth.models import Group
from customers.models import UserAccessGroup
from orders.models import Item, Order
from customers.models import Customer
from .views import ItemViewSet, OrderViewSet


def user_account(email, password):
    password = make_password(password)
    user, created = get_user_model().objects.get_or_create(
        email=email, first_name="Test", last_name="User", password=password
    )
    return user


class TestOrderApp(APITestCase, TestCase):
    token: dict
    user: Customer
    group: Group
    user_access_group = UserAccessGroup
    item = Item
    email = "testb@user.com"
    password = "@QAZwsxedc."

    def getToken(self, email, password):
        data = {"email": email, "password": password}
        return self.client.post("/api/token/", data).json()

    def createAccessGroup(self):
        Group.objects.create(name="admin_access")
        self.group = Group.objects.filter(name="admin_access").first()
        self.user_access_group = UserAccessGroup.objects.create(
            user_id=self.user.id, group_id=self.group.id
        )

    def setUp(self):
        self.user = user_account(self.email, self.password)
        self.createAccessGroup()
        self.token = self.getToken(self.email, self.password)

        factory = APIRequestFactory()
        request = factory.post(
            "api/admin/items/",
            {"name": "food_b", "amount": 300, "available": True},
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = ItemViewSet.as_view({"post": "create"})
        response = view(request)
        self.item = response.data

    def item_creation(self):
        factory = APIRequestFactory()
        request = factory.post(
            "api/admin/items/",
            {"name": "food_b", "amount": 300, "available": True},
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = ItemViewSet.as_view({"post": "create"})
        response = view(request)
        return response.data

    def test_item_creation(self):
        factory = APIRequestFactory()
        request = factory.post(
            "api/admin/items/",
            {"name": "food_d", "amount": 590, "available": True},
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = ItemViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="failed to create item",
        )

    def test_fetch_items(self):
        factory = APIRequestFactory()
        request = factory.get(
            "api/admin/items/",
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = ItemViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed to fetch items"
        )

    def test_fetch_item(self):
        factory = APIRequestFactory()
        item = self.item_creation()
        request = factory.get(
            "api/admin/items/{}/".format(item["id"]),
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = ItemViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed fetch an item"
        )

    def test_patch_item(self):
        factory = APIRequestFactory()
        item = self.item_creation()
        data = {"name": "fooduu_d", "amount": 230, "available": False}
        response = self.client.patch(
            "/api/admin/items/{}/".format(item["id"]),
            data=data,
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed patch item"
        )

    def test_update_item(self):
        factory = APIRequestFactory()
        item = self.item_creation()
        data = {"name": "new food", "amount": 2700, "available": True}
        response = self.client.put(
            "/api/admin/items/{}/".format(item["id"]),
            data=data,
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed update an item"
        )

    def test_delete_item(self):
        factory = APIRequestFactory()
        item = self.item_creation()
        data = {"name": "another food", "amount": 650, "available": True}
        response = self.client.delete(
            "/api/admin/items/{}/".format(item["id"]),
            data={},
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            msg="failed to delete an item",
        )

    # TEST FOR ORDER

    def order_creation(self):
        factory = APIRequestFactory()
        request = factory.post(
            "api/admin/orders/",
            {"customer": self.user.id, "item": self.item.get("id")},
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = OrderViewSet.as_view({"post": "create"})
        return view(request).data

    def test_order_creation(self):
        factory = APIRequestFactory()
        request = factory.post(
            "api/admin/orders/",
            {"customer": self.user.id, "item": self.item.get("id")},
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = OrderViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg="failed to create order"
        )

    def test_fetch_orders(self):
        self.order_creation()
        factory = APIRequestFactory()
        request = factory.get(
            "api/admin/orders/",
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = OrderViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed to fetch orders"
        )

    def test_fetch_order(self):
        factory = APIRequestFactory()
        order = self.order_creation()
        request = factory.get(
            "api/admin/orders/{}/".format(order["id"]),
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = OrderViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed to fetch an order"
        )

    def test_patch_order(self):
        factory = APIRequestFactory()
        item = self.item_creation()
        order = self.order_creation()
        data = {"customer": self.user.id, "item": item.get("id")}
        response = self.client.patch(
            "/api/admin/orders/{}/".format(order["id"]),
            data=data,
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed patch an order"
        )

    def test_update_order(self):
        factory = APIRequestFactory()
        order = self.order_creation()
        item = self.item_creation()
        data = {"customer": self.user.id, "item": item.get("id")}
        response = self.client.put(
            "/api/admin/orders/{}/".format(order["id"]),
            data=data,
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed to update an order"
        )

    def test_delete_order(self):
        factory = APIRequestFactory()
        order = self.order_creation()
        response = self.client.delete(
            "/api/admin/orders/{}/".format(order["id"]),
            data=order,
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            msg="failed delete an order",
        )
