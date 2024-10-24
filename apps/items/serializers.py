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
    # Accept the category_id and unit_id in the input but return their names in the response
    category = serializers.CharField(source='category.name', read_only=True)
    unit = serializers.CharField(source='unit.name', read_only=True)
    category_id = serializers.IntegerField(write_only=True)  # Accept category_id on create
    unit_id = serializers.IntegerField(write_only=True)  # Accept unit_id on create

    class Meta:
        model = Item
        fields = ['id', 'user', 'name', 'description', 'barcode', 'category', 'quantity', 'price', 'reorder_quantity', 'unit', 'date_added', 'last_updated', 'category_id', 'unit_id']

class ArchiveSerializer(serializers.ModelSerializer):
    # Accept the category_id and unit_id in the input but return their names in the response
    category = serializers.CharField(source='category.name', read_only=True)
    unit = serializers.CharField(source='unit.name', read_only=True)
    category_id = serializers.IntegerField(write_only=True)  # Accept category_id on create
    unit_id = serializers.IntegerField(write_only=True)  # Accept unit_id on create

    class Meta:
        model = Item
        fields = ['id', 'user', 'name', 'description', 'barcode', 'category', 'quantity', 'price', 'reorder_quantity', 'unit', 'date_added', 'last_updated', 'category_id', 'unit_id']
