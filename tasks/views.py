from django.shortcuts import render
from .models import Category, Task

def index(request):
    category_list = Category.objects.order_by('id')
    tasks_list = Task.objects.order_by('id')
    context = {'category_list': category_list,
               'tasks_list': tasks_list}
    return render(request, 'index.html', context)

def category(request, name):
    description = ''
    category_list = Category.objects.order_by('id')
    for category in category_list:
        if category.name == name:
            description = category.description
            break
    
    #tasks_list = Task.objects.all()
    #tasks_list = tasks_list.filter(category=name)

    #tasks_list = Task.objects.raw(f'SELECT Tasks FROM TASKS WHERE category={name}')
    tasks_list = []
    for task in Task.objects.all():
        if str(name) == str(task.category):
            tasks_list.append(task)


    context = {
        'name': name,
        'description': description,
        'tasks': tasks_list,
        }
    return render(request, 'category.html', context )

def task(request, name):
    description = ''
    created_date = ''
    finish_date = ''
    category = ''
    complete = ''

    tasks_list = Task.objects.order_by('id')
    for task in tasks_list:
        if task.title == name:
            description = task.content
            created_date = task.created_date
            finish_date = task.finish_date
            category = task.category
            complete = task.complete
    
    context = {
        'name': name,
        'description': description,
        'created_date': created_date,
        'finish_date': finish_date,
        'category': category,
        'complete': complete,
        }
    return render(request, 'task.html', context )



