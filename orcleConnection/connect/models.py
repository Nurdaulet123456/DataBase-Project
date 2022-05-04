from email.mime import image
from email.policy import default
from django.db import models
# Create your models here.



class Bank_card(models.Model):
    bank_name = models.CharField(max_length=100)
    bank_commission_percent = models.FloatField()
    total_transactions = models.IntegerField()


class Other_offices(models.Model):
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    number = models.CharField(max_length=100)



class Discounts(models.Model):
    discount_id = models.CharField(max_length=100)
    percent = models.FloatField()
    starter_sum = models.IntegerField()


class Consultants(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    sales_sum = models.IntegerField()
    image = models.ImageField(default="https://via.placeholder.com/300x300")



class Product_Types(models.Model):
    type_name = models.CharField(max_length=100)
    amount = models.IntegerField()
    image = models.ImageField(default="https://via.placeholder.com/300x300")




