from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=60, null=False)
    phone = models.CharField(max_length=20, null=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    def __str__(self):
        return self.name

class Menu_Price(models.Model):
    menu = models.CharField(max_length=45)
    price = models.CharField(max_length=10)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.menu