from django.db import models
from django.contrib.auth.models import User

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.name} (x{self.quantity})'