from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(blank=True,null=True)
    description = models.CharField(max_length=300)
    in_cart = models.BooleanField(default=False)
    image = models.CharField(blank=True, null=True, max_length=400)
    def __str__(self):
        return self.name

class Cart(models.Model):
    #current_user =  models.ForeignKey(User, on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    itemtotal=models.FloatField(blank=True,null=True)
    #
    # def __str__(self):
    #     return str(self.current_user.username)

    def get_total_item_price(self):
        return self.quantity*self.item.price


