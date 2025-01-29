from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
import random


# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



def generate_staff_id():
    return f"S{random.randint(1000, 9999)}"

class StaffUser(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    random_id = models.CharField(max_length=5, unique=True, default=generate_staff_id)  # Generate a 4-digit ID
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.random_id})"
    


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # Stock field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
