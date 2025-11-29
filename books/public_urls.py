from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.book_search, name='book_search'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
]
