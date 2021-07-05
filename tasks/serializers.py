from rest_framework import serializers
from .models import Category, Task

class Category_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class Task_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'content', 'created_date', 'finish_date', 'category', 'complete')