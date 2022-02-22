from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', views.project, name='project'),
    path('add-new-project/', views.createProject, name='create_form'),
    path('update-project/<str:pk>/', views.updateProject, name='update_form'),
    path('delete-project/<str:pk>/', views.deleteProject, name='delete_form')
]