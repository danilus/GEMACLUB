from django.urls import path

from . import views


app_name = 'club'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('socios/', views.member_list, name='member_list'),
    path('socios/crear/', views.member_create, name='member_create'),
    path('socios/<int:pk>/editar/', views.member_edit, name='member_edit'),
    path('socios/<int:pk>/eliminar/', views.member_delete, name='member_delete'),
]
