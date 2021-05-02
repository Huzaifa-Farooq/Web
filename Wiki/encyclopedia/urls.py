from django.urls import path
from . import views

app_name = "wiki"
urlpatterns = [
    path('search/', views.search, name='search'),
    path("", views.index, name="index"),
    path("create_new_page", views.create_new_page, name="create_new_page"),
    path("random", views.random_page, name="random_page"),
    path("edit/<str:page_title>", views.edit_page, name="edit_page"),
    path(f"<str:title>", views.show_entry, name="show_entry"),
]
