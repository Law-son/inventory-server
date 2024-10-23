from rest_framework import serializers
from .models import Category, Unit, Item, Archive

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'barcode', 'category', 'quantity', 'price', 'reorder_quantity', 'unit', 'date_added', 'last_updated']

class ArchiveSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = Archive
        fields = ['id', 'name', 'description', 'barcode', 'category', 'quantity', 'price', 'reorder_quantity', 'unit', 'date_added', 'last_updated']
