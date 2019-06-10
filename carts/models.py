from django.db import models
from products.models import Product
import uuid
import json


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    products = models.TextField(default="{}")
    updated = models.DateTimeField(auto_now=True)

    def get_products(self):
        result = {}
        cart_products = json.loads(self.products)
        for p in Product.objects.filter(pk__in=[int(p_id) for p_id in cart_products.keys()]):
            result.update({p: cart_products[str(p.id)]})
        return result


class Invoice(models.Model):
    # FIXME нужно заменить стандартную функцию delete чтобы вернуть товар на склад
    id = models.BigAutoField
    products = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
