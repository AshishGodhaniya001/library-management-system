from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
# near other imports at top of file
from django.db.models import Count, Sum, Q

from accounts.utils import is_librarian_or_admin
from books.models import Book
from .models import Issue


@login_required
def request_issue(request, book_id):
    """Student: send issue request for a book"""
    book = get_object_or_404(Book, id=book_id)

    # Only students allowed (optional but good)
    role = getattr(request.user, "role", "student")
    if role != "student":
        messages.error(request, "Only students can request books.")
        return redirect("book_detail", pk=book_id)

    # No copies available
    if book.available_copies < 1:
        messages.error(request, "No copies available.")
        return redirect("book_detail", pk=book_id)

    # Prevent multiple active request/issue for same book
    existing = Issue.objects.filter(
        user=request.user,
        book=book,
        status__in=["requested", "issued", "overdue"],
    ).exists()

    if existing:
        messages.warning(request, "You already have an active request/issue for this book.")
        return redirect("book_detail", pk=book_id)

    # Limit total active issues
    active_count = Issue.objects.filter(
        user=request.user,
        status__in=["requested", "issued", "overdue"],
    ).count()
    MAX_ACTIVE_ISSUES = 3
    if active_count >= MAX_ACTIVE_ISSUES:
        messages.error(
            request,
            f"You cannot have more than {MAX_ACTIVE_ISSUES} active book issues/requests.",
        )
        return redirect("my_issues")

    Issue.objects.create(
        user=request.user,
        book=book,
        status="requested",
    )
    messages.success(request, "Issue request submitted successfully.")
    return redirect("book_detail", pk=book_id)


@login_required
def my_issues(request):
    """Student: see all own issues/requests"""
    issues = Issue.objects.filter(user=request.user).order_by("-request_date")
    return render(request, "transactions/my_issues.html", {"issues": issues})
@login_required
def student_dashboard(request):
    user = request.user
    issued = Issue.objects.filter(user=user, status='issued').order_by('-issue_date')
    requested = Issue.objects.filter(user=user, status='requested').order_by('-request_date')
    returned = Issue.objects.filter(user=user, status='returned').order_by('-return_date')

    total_issued = issued.count()
    total_fine = Issue.objects.filter(user=user).aggregate(total=Sum('fine_amount'))['total'] or 0
    overdue_count = Issue.objects.filter(user=user, status='issued', due_date__lt=timezone.now()).count()

    context = {
        'issued': issued,
        'requested': requested,
        'returned': returned,
        'total_issued': total_issued,
        'total_fine': total_fine,
        'overdue_count': overdue_count,
    }
    return render(request, "transactions/student_dashboard.html", context)



@user_passes_test(is_librarian_or_admin)
def manage_requests(request):
    """Librarian/Admin: see all pending requests + issued books"""
    pending = Issue.objects.filter(status="requested").order_by("request_date")
    issued = Issue.objects.filter(status="issued").order_by("issue_date")

    return render(
        request,
        "transactions/manage_requests.html",
        {"pending": pending, "issued": issued},
    )

@user_passes_test(is_librarian_or_admin)
def approve_issue(request, issue_id):
    """Librarian/Admin: approve a pending request and mark as issued"""
    issue = get_object_or_404(Issue, id=issue_id)
    book = issue.book

    if book.available_copies < 1:
        messages.error(request, "No copies available for this book.")
        return redirect("manage_requests")

    issue.status = "issued"
    issue.issue_date = timezone.now()
    issue.due_date = timezone.now() + timedelta(days=7)  # 7 days default
    issue.save()

    book.available_copies -= 1
    book.save()

    messages.success(request, "Issue approved.")
    return redirect("manage_requests")


@user_passes_test(is_librarian_or_admin)
def mark_returned(request, issue_id):
    """Librarian/Admin: mark a book as returned and calculate fine"""
    issue = get_object_or_404(Issue, id=issue_id)
    book = issue.book

    issue.status = "returned"
    issue.return_date = timezone.now()

    # Fine calculate (₹10 per day)
    fine = issue.calculate_fine(rate_per_day=10)
    issue.fine_amount = fine
    issue.save()

    book.available_copies += 1
    book.save()

    if fine > 0:
        messages.warning(request, f"Book returned. Fine applicable: ₹{fine}.")
    else:
        messages.success(request, "Book returned. No fine.")

    return redirect("manage_requests")
@user_passes_test(is_librarian_or_admin)
def librarian_dashboard(request):
    total_books = Book.objects.aggregate(total=Sum('total_copies'))['total'] or 0
    total_available = Book.objects.aggregate(total=Sum('available_copies'))['total'] or 0
    pending = Issue.objects.filter(status='requested').order_by('request_date')
    issued = Issue.objects.filter(status='issued').order_by('-issue_date')

    low_stock = Book.objects.filter(available_copies__lte=2).order_by('available_copies')[:8]
    category_counts = list(
        Book.objects.values('category__name').annotate(count=Count('id')).order_by('-count')
    )

    context = {
        'total_books': total_books,
        'total_available': total_available,
        'pending': pending,
        'issued': issued,
        'low_stock': low_stock,
        'category_counts': category_counts,
    }
    return render(request, "transactions/librarian_dashboard.html", context)