from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Big_Category(models.Model):
    name = models.CharField(max_length=45)

class Category(models.Model):
    name = models.CharField(max_length=30)
    big_category = models.ForeignKey(Big_Category, on_delete=models.SET_NULL,blank=True, null=True, related_name='big_category')

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=60, null=False)
    phone = models.CharField(max_length=20, null=True)
    rating = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, default=None, related_name='owner')

    def __str__(self):
        return self.name
    
    def short_name(self):
        first_name = self.name.split()[0]
        if len(self.name) >= 7:
            if '이문' in self.name.split()[0] :
                first_name = first_name.replace('이문', ' ')
            if '외대' in self.name:
                first_name = first_name.replace('외대', ' ')
            return self.name.split()[0]
        else:
            return self.name

class Menu_Price(models.Model):
    menu = models.CharField(max_length=45)
    price = models.CharField(max_length=10)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, null=False, blank=False, related_name="restaurant")

    def __str__(self):
        return self.menu