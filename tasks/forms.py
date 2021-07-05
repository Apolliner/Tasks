from django import forms 
from django.utils import timezone
from .models import Category, Task

class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'

class CategoryForm(forms.Form):
    name = forms.CharField(label='Name category', max_length=40)
    description = forms.CharField(label='Description category', max_length=1000)
class TaskForm(forms.Form):
    category_list = Category.objects.order_by('id')
    category_name_list = []
    for category in category_list:
        category_name_list.append((str(category.name), str(category.name)))
    print(F"category_name_list - {category_name_list}")
    title = forms.CharField(label='Name task', max_length=40)
    content = forms.CharField(label='Description task', max_length=1000)
    finish_date = forms.DateField(label='Finish date', widget=MyDateInput({'class': 'form-control'}))
    category = forms.ChoiceField(label='Category', choices = category_name_list)




