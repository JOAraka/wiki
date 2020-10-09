from django.urls import path
from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki/<str:title>", views.wiki, name="get"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search"),
]
