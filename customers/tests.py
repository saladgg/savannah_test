from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIRequestFactory, APITestCase
from unittest import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from django.contrib.auth.models import Group
from customers.models import UserAccessGroup
from customers.models import Customer
from .views import CustomerViewSet


def user_account(email, password):
    password = make_password(password)
    user, created = get_user_model().objects.get_or_create(
        email=email, first_name="Test", last_name="User", password=password
    )
    return user


class TestCustomerApp(APITestCase, TestCase):
    token: dict
    user: Customer
    group: Group
    user_access_group = UserAccessGroup
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

    def customer_creation(self):
        factory = APIRequestFactory()
        request = factory.post(
            "api/admin/customers/",
            {
                "first_name": "fatuma",
                "last_name": "dida",
                "email": "fatuda@gmail.com",
                "phone": "0727999111",
            },
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = CustomerViewSet.as_view({"post": "create"})
        response = view(request)
        return response.data

    def test_customer_creation(self):
        factory = APIRequestFactory()
        request = factory.post(
            "api/admin/customers/",
            {
                "first_name": "abdi",
                "last_name": "hamza",
                "email": "hamzadi@gmail.com",
                "phone": "0727999111",
            },
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = CustomerViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="failed to create customer",
        )

    def test_fetch_customers(self):
        factory = APIRequestFactory()
        request = factory.get(
            "api/admin/customers/",
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = CustomerViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed to fetch customers"
        )

    def test_fetch_customer(self):
        factory = APIRequestFactory()
        customer = self.customer_creation()
        request = factory.get(
            "api/admin/customers/{}/".format(customer["id"]),
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        view = CustomerViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed fetch the customer"
        )

    def test_patch_customer(self):
        factory = APIRequestFactory()
        customer = self.customer_creation()
        data = {"first_name": "kazuma", "phone": "0727000666"}
        response = self.client.patch(
            "/api/admin/customers/{}/".format(customer["id"]),
            data=data,
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed patch customer"
        )

    def test_update_customer(self):
        factory = APIRequestFactory()
        customer = self.customer_creation()
        data = {
            "first_name": "salad",
            "last_name": "guyo",
            "email": "saguyo@gmail.com",
            "phone": "0729777555",
        }
        response = self.client.put(
            "/api/admin/customers/{}/".format(customer["id"]),
            data=data,
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="failed update customer"
        )

    def test_delete_customer(self):
        factory = APIRequestFactory()
        customer = self.customer_creation()
        response = self.client.delete(
            "/api/admin/customers/{}/".format(customer["id"]),
            data={},
            HTTP_AUTHORIZATION="Bearer {}".format(self.token["access"]),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            msg="failed to delete customer",
        )
