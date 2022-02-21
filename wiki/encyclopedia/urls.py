"""urls.py"""
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/edit", views.edit, name = "edit"),
    path("create", views.create, name = "create"),
    path("random", views.random_page, name = "random"),
    path("search", views.search, name = "search" ),
    # url path to display entry contents at /wiki/TITLE
    path("wiki/<str:entry>", views.entry, name="entry"),
]
