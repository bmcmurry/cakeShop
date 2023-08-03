from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    profile_pic = models.ImageField(
        default="profile_pic_green.png", null=True, blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ("Cake", "Cake"),
        ("Cookie", "Cookie"),
        ("Pie", "Pie"),
        ("Cupcake", "Cupcake"),
    )

    name = models.CharField(max_length=50)
    price = models.FloatField()
    category = models.CharField(max_length=50, null=True, choices=CATEGORY)
    description = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        default="It's made with Sugar, Spice, and Everything Nice.",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Out For Delivery", "Out For Delivery"),
        ("Delivered", "Delivered"),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.product.name
