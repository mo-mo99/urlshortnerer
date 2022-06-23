from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all-links', views.show_links, name='show'),
    path('<slug:slug>', views.get_slug, name='getslug'),
    path('delete/<int:id>', views.delete_link, name='delete')
    
]