"""ToDo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('category/<str:name>/', views.category, name='<str:name>'),
    path('tasks/<int:id>/', views.task, name='<int:id>'),
    path('category/add', views.add_category, name='add category'),
    path('tasks/add', views.add_task, name='add task'),
    path('complete/<task_id>', views.complete_task, name='complete'),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
