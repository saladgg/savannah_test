import random, uuid, string, time
from django.db import models
from django.contrib.auth.models import Group, AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


def getCode():
    ms = int(time.time() * 1000.0)
    rand_1 = "".join(
        random.choices(string.ascii_uppercase + string.digits + str(ms), k=9)
    )
    return rand_1


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email is required."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class Customer(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=100, default="NEWCUSTOMER")
    updated_on = models.DateTimeField(auto_now=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("id",)


class UserAccessGroup(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.group.name

    class Meta:
        ordering = ("id",)
