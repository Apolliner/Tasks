from django.shortcuts import render, redirect
from .models import Category, Task
from .forms import CategoryForm, TaskForm

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
    
    tasks_list = []
    for task in Task.objects.all():
        if str(name) == str(task.category):
            tasks_list.append(task)
    context = {
        'name': name,
        'description': description,
        'tasks': tasks_list,
        'type': 'category',
        }
    return render(request, 'category.html', context )

def task(request, id):
    description = ''
    created_date = ''
    finish_date = ''
    category = ''
    complete = ''
    task_id = ''

    tasks_list = Task.objects.order_by('id')
    for task in tasks_list:
        if task.id == id:
            title = task.title
            description = task.content
            created_date = task.created_date
            finish_date = task.finish_date
            category = task.category
            complete = task.complete
            task_id = task.id
    
    context = {
        'name': title,
        'description': description,
        'created_date': created_date,
        'finish_date': finish_date,
        'category': category,
        'complete': complete,
        'task_id': task_id,
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



