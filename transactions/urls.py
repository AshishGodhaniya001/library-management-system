from django.urls import path
from . import views

urlpatterns = [
    path('request/<int:book_id>/', views.request_issue, name='request_issue'),
    path('my-issues/', views.my_issues, name='my_issues'),
    path('manage/', views.manage_requests, name='manage_requests'),
    path('approve/<int:issue_id>/', views.approve_issue, name='approve_issue'),
    path('return/<int:issue_id>/', views.mark_returned, name='mark_returned'),
    
path('dashboard/', views.student_dashboard, name='student_dashboard'),
path('librarian/', views.librarian_dashboard, name='librarian_dashboard'),
]
