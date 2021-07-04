from django.db import models
from django.utils import timezone
import random

class Category(models.Model):
    name = models.CharField(max_length=40, default='general')
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Task(models.Model):
	title = models.CharField(max_length=250)
	content = models.TextField(blank=True) #текстовое поле
	created_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # дата создания
	finish_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) #до какой даты нужно было сделать дело
	category = models.ForeignKey(Category, default="general",on_delete=models.PROTECT) # foreignkey с помощью которой мы будем осуществлять связь с таблицей Категорий
	complete = models.BooleanField(default=False)
	class Meta: #используем вспомогательный класс мета для сортировки наших дел
		ordering = ["-created_date"] #сортировка дел по времени их создания
	def __str__(self):
		return self.title