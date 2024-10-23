from django.db import models
from apps.accounts.models import User  # Importing the User model from the accounts app


# Model class for Categories
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Make user optional
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model class for Units
class Unit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Make user optional
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model class for Item
class Item(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the item
    name = models.CharField(max_length=200)  # Name of the item
    description = models.TextField()  # Detailed description of the item
    barcode = models.CharField(max_length=200, blank=True, null=True)  # Barcode for the item, optional
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Category to which the item belongs
    quantity = models.IntegerField()  # Current stock level
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the item
    reorder_quantity = models.IntegerField(blank=True, null=True)  # Amount to reorder when stock is low
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)  # Measurement unit
    date_added = models.DateTimeField(auto_now_add=True)  # Timestamp of when the item was added
    last_updated = models.DateTimeField(auto_now=True)  # Timestamp of the last update

    def __str__(self):
        return self.name

# Model class for Archive
class Archive(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    barcode = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_quantity = models.IntegerField(blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

