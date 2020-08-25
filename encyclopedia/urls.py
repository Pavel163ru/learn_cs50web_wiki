from django.urls import path

from . import views

# app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("editpage/<slug:title>", views.editpage, name="editpage"),
    path("randompage", views.randompage, name="randompage"),
    path("wiki/<str:title>", views.entry, name="entry")   
]
