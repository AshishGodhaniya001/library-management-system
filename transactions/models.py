from django.db import models
from django.conf import settings
from django.utils import timezone
from books.models import Book

class Issue(models.Model):
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('rejected', 'Rejected'),
        ('overdue', 'Overdue'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    request_date = models.DateTimeField(auto_now_add=True)
    issue_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user} -> {self.book} ({self.status})"
    def calculate_fine(self, rate_per_day=10):
        """Calculate fine based on due_date and return_date (or today)."""
        if not self.due_date:
            return 0

        # Agar return_date set hai to usko use karo, nahi to abhi ka time
        ref_date = self.return_date or timezone.now()

        if ref_date <= self.due_date:
            return 0

        diff = ref_date - self.due_date
        late_days = diff.days
        if late_days < 1:
            return 0

        return late_days * rate_per_day
