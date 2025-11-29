from django.urls import path
from . import views

urlpatterns =[
    path('search/', views.book_search, name='book_search'),
    # other book urls...
]

