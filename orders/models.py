import random,uuid,string,time
from django.db import models
from customers.models import Customer


class Item(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    available = models.BooleanField(default=False)
    added_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ('id',)




class Order(models.Model):
    id = models.UUIDField(default= uuid.uuid4, primary_key=True, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL,null=True)
    added_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.customer.email


    class Meta:
        ordering = ('added_on',)


