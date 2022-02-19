"""docstring"""
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    # url path to display entry contents at /wiki/TITLE
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name = "search" )
]
