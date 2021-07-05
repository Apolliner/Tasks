from django.urls import include, path, re_path
from rest_framework import routers, permissions
from . import views
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.DefaultRouter()
router.register(r'Category', views.CategoryViewSet)
router.register(r'Task', views.TaskViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/<int:id>/', views.task, name='<int:id>'),
    path('category/add', views.add_category, name='add category'),
    path('tasks/add', views.add_task, name='add task'),
    path('category/<str:name>/', views.category, name='<str:name>'),
    path('rest_view/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('create-category/', views.CategoryCreateView.as_view(), name=None),
    path('category-<int:pk>/', views.CategoryDetailView.as_view(), name=None),
    path('category/<str:name>/', views.Category, name='<str:name>'),
    path('create-task/', views.TaskCreateView.as_view(), name=None),
    path('task-<int:pk>/', views.TaskDetailView.as_view(), name=None),
    path('task/<str:name>/', views.Task, name=None),
    path('csv-save/', views.CSVPageView.as_view(), name='csv_save_page'),
    path('export/csv-database-write/', views.csv_database_write, name='csv_database_write'),
    path('export/csv-database-read/', views.csv_database_read, name='csv_database_read'),
    path('delete_category/<int:id>', views.delete_category, name='delete_category'),
    path('edit_category/<int:id>', views.edit_category, name='edit_category'),
    path('delete_task/<int:id>', views.delete_task, name='delete_task'),
    path('edit_task/<int:id>', views.edit_task, name='edit_task'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]   