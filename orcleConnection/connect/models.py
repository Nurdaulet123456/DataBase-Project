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
    phone_number = models.CharField(max_length=100)


class Discounts(models.Model):
    discount_id = models.CharField(max_length=100)
    percent = models.FloatField()
    starter_sum = models.IntegerField()


class Consultants(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    sales_sum = models.IntegerField(default=0)
    image = models.ImageField(default="img/default-avatar.jpg")

class Product_Types(models.Model):
    type_name = models.CharField(max_length=100)
    amount = models.IntegerField()
    image = models.ImageField(default="zhai.jpg")

class Articles(models.Model):
    article = models.CharField(max_length=50, primary_key=True)
    type = models.ForeignKey(Product_Types, on_delete=models.CASCADE)
    XS = models.IntegerField()
    S = models.IntegerField()
    L = models.IntegerField()
    M = models.IntegerField()
    price = models.IntegerField()
    gender = models.CharField(max_length=20)

class Customers(models.Model):
    gender_choices = (('M', 'Male'),
                      ('F', 'Female'))
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices=gender_choices, max_length=2)
    bank_card_no = models.CharField(max_length=20, blank=True)
    expiration_date = models.CharField(max_length=15, blank=True)
    CVV = models.CharField(max_length=3, blank=True)
    total_purchases = models.IntegerField(default=0)
    bank_card = models.ForeignKey(Bank_card, on_delete=models.CASCADE)
    discount_id = models.CharField(max_length=3, blank=True)

class Customers_Purchase(models.Model):
    purchase_id = models.IntegerField(primary_key=True)
    cust = models.ForeignKey(Customers, on_delete=models.CASCADE)
    consultant = models.ForeignKey(Consultants, on_delete=models.CASCADE)
    data = models.DateField()
    total_sum = models.IntegerField()

class Purchases(models.Model):
    purchase_id = models.IntegerField()
    article = models.ForeignKey(Articles, on_delete=models.PROTECT)
    sizes = models.CharField(max_length=5)
    amount = models.IntegerField()

