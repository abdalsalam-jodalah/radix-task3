from django.urls import path
from ..controllers.task_category_controllers import TaskCategoryApi

urlpatterns = [
    path('category/', TaskCategoryApi.as_view(), name='category-crud'),
    path('category/<int:pk>/', TaskCategoryApi.as_view(), name='category-detail'), 
      ]