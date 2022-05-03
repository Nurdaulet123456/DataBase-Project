from django.db import models
# Create your models here.


class Doctor(models.Model):
    text = models.CharField(max_length=60, null=True)
    image = models.ImageField()


    def __str__(self):
        return self.text


class Product(models.Model):
    change = models.CharField(max_length=100)

class Shop(models.Model):
    shop = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.shop