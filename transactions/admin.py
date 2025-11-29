from django.contrib import admin
from .models import Issue

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status', 'issue_date', 'due_date', 'return_date', 'fine_amount')
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')
