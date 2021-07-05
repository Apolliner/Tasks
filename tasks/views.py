from django.shortcuts import render, redirect
from .models import Category, Task
from . import serializers
from .forms import CategoryForm, TaskForm
from .serializers import Category_serializer, Task_serializer
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from django.views.generic.base import TemplateView
from django.http import HttpResponse 
import csv 
import os


def csv_database_write(request):
    """
        Запись объектов датабазы в файл CSV
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_database.csv"'
    writer = csv.writer(response)
    for category in Category.objects.all():
        writer.writerow(['category', category.id, category.name, category.description])
    for task in Task.objects.all():
        writer.writerow(['task', task.id, task.title, task.content, task.created_date, task.finish_date, task.category, task.complete])
    return response

def csv_database_read(request):
    """
        Загрузка объектов из файла. Проверка, есть ли совпадения с базой данных, добавление их в базу данных, если их там нет
    """
    path = os.path.dirname(__file__)
    file = os.path.join(path, '../csv_database.csv')

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if row[0] == 'category':
                category_not_in_db = True
                for category in Category.objects.all():
                    if str(category.name) == row[2] and str(category.description) == row[3]:
                        category_not_in_db = False
                if category_not_in_db: #Если категории нет в датабазе, то сохраняем
                    new_category = Category(name=row[2], description=row[3])
                    new_category.save()
            else: # task
                task_not_in_db = True
                for task in Task.objects.all():
                    if str(task.title) == row[2] and str(task.content) == row[3]:
                        task_not_in_db = False
                if task_not_in_db: #Если задачи нет в датабазе, то сохраняем
                    for category in Category.objects.order_by('id'):
                        if str(category.name) == row[6]:
                            new_task = Task(title=row[2], content=row[3], created_date=row[4], finish_date=row[5], category=category, complete=row[7])
                            new_task.save()
            line_count += 1
        return redirect('../../')

class CSVPageView(TemplateView):
    template_name = "csv_save.html"

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = Category_serializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('id')
    serializer_class = Task_serializer

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.Category_serializer
    def create(self, request, *args, **kwargs):
        super(CategoryCreateView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully created",
                    "result": request.data}
        return Response(response)

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.Task_serializer
    def create(self, request, *args, **kwargs):
        super(TaskCreateView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully created",
                    "result": request.data}
        return Response(response)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.Category_serializer
    def retrieve(self, request, *args, **kwargs):
        super(CategoryDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)
    def patch(self, request, *args, **kwargs):
        super(CategoryDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully updated",
                    "result": data}
        return Response(response)
    def delete(self, request, *args, **kwargs):
        super(CategoryDetailView, self).delete(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully deleted"}
        return Response(response)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.Task_serializer
    def retrieve(self, request, *args, **kwargs):
        super(TaskDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)
    def patch(self, request, *args, **kwargs):
        super(TaskDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully updated",
                    "result": data}
        return Response(response)
    def delete(self, request, *args, **kwargs):
        super(TaskDetailView, self).delete(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully deleted"}
        return Response(response)




def index(request):
    category_list = Category.objects.order_by('id')
    tasks_list = Task.objects.order_by('id')
    context = {'category_list': category_list,
               'tasks_list': tasks_list}
    return render(request, 'index.html', context)

def category(request, name):
    description = ''
    id = ''
    category_list = Category.objects.order_by('id')
    for category in category_list:
        if category.name == name:
            description = category.description
            id = category.id
            break
    
    tasks_list = []
    for task in Task.objects.all():
        if str(name) == str(task.category):
            tasks_list.append(task)
    context = {
        'name': name,
        'description': description,
        'tasks': tasks_list,
        'type': 'category',
        'id': id,
        }
    return render(request, 'category.html', context )

def task(request, id):
    description = ''
    created_date = ''
    finish_date = ''
    category = ''
    complete = ''

    tasks_list = Task.objects.order_by('id')
    for task in tasks_list:
        if task.id == id:
            title = task.title
            description = task.content
            created_date = task.created_date
            finish_date = task.finish_date
            category = task.category
            complete = task.complete
    
    context = {
        'name': title,
        'description': description,
        'created_date': created_date,
        'finish_date': finish_date,
        'category': category,
        'complete': complete,
        'id': id,
        'type': 'task',
        }
    return render(request, 'task.html', context )

def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            title = request.POST.get("title")
            content = request.POST.get("content")
            finish_date = request.POST.get("finish_date")
            name_category = request.POST.get("category")
            for category in Category.objects.order_by('id'):
                if str(category.name) == name_category:
                    new_task = Task(title=title, content=content, finish_date=finish_date, category=category)
                    new_task.save()
            

        return redirect('index')
    else:
        form = TaskForm()
        context = {
            'form' : form,
            'description' : 'task'
            }
        return render(request, 'add.html', context)

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            description = request.POST.get("description")
            new_category = Category(name=name, description=description)
            new_category.save()
        return redirect('index')
    else:
        form = CategoryForm()
        context = {
            'form' : form,
            'description' : 'category'
            }
        return render(request, 'add.html', context)

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.complete = True
    task.save()

    return redirect('index')

def edit_category(request, id):
    try:
        category = Category.objects.get(id=id)
        if request.method == "POST":
            print(F'\n \n \n \n request.POST.get("name") - {request.POST.get("name")}, request.POST.get("description") - {request.POST.get("description")}')
            if str(request.POST.get("name")) != 'None':
                category.name = request.POST.get("name")
            if str(request.POST.get("description")) != 'None':
                category.description = request.POST.get("description")
            category.save()
            return redirect("/")
        else:
            return render(request, "edit.html", {"category": category, 'type': 'category'})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>category not found</h2>")

def edit_task(request, id):
    try:
        task = Task.objects.get(id=id)
        if request.method == "POST":
            task.title = request.POST.get("title")
            task.content = request.POST.get("content")
            task.finish_date = request.POST.get("finish_date")
            task.save()
            return redirect("/")
        else:
            return render(request, "edit.html", {"task": task, 'type': 'task'})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>task not found</h2>")
     
# удаление данных из бд
def delete_category(request, id):
    try:
        category = Category.objects.get(id=id)
        for task in Task.objects.all():
            if str(task.category) == str(category.name): #Удаление всех задач из удаляемой категории
                task.delete()
        category.delete()
        return redirect('index')
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>category not found</h2>")
def delete_task(request, id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        return redirect('index')
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>task not found</h2>")



