from django.urls import path

from . import views


app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    #
    path('institucional/', views.institutional_overview, name='institutional_overview'),
    path("institucional/autoridades/", views.authorities, name="authorities"),
    path("institucional/estatuto/", views.statute, name="statute"),
    #
    path('disciplinas/', views.disciplines, name='disciplines'),
    #
    path('articulos/', views.articles, name='articles'),
 ]