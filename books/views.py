from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
import json

from .models import Book, Category, Review, UserLibrary
from .forms import BookForm, ReviewForm, UserRegistrationForm

# ----------------- WEB VIEWS -----------------

def home_view(request):
    """Landing Page (Home UI from BookSphere)."""
    if request.method == 'POST':
        messages.success(request, "Thank you for getting in touch! Our team will respond shortly.")
        return redirect('home')

    books = Book.objects.all()[:8]
    categories = Category.objects.all()
    total_books = Book.objects.count()

    context = {
        'books': books,
        'categories': categories,
        'total_books': total_books,
    }
    return render(request, 'home.html', context)

def ebook_view(request):
    """E-Books Catalog & Search UI."""
    books = Book.objects.all()
    categories = Category.objects.all()

    q = request.GET.get('q', '').strip()
    if q:
        books = books.filter(
            Q(title__icontains=q) |
            Q(author__icontains=q) |
            Q(description__icontains=q)
        )

    category_slug = request.GET.get('category', '').strip()
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=active_category)

    user_saved_ids = []
    if request.user.is_authenticated:
        user_saved_ids = list(request.user.saved_books.values_list('book_id', flat=True))

    context = {
        'books': books,
        'categories': categories,
        'active_category': active_category,
        'q': q,
        'user_saved_ids': user_saved_ids,
        'total_count': books.count(),
    }
    return render(request, 'ebook.html', context)

def about_view(request):
    """About Us Page."""
    return render(request, 'about.html')

def download_view(request):
    """Download Page."""
    books = Book.objects.all()
    return render(request, 'download.html', {'books': books})

def reviews_view(request):
    """Community Reviews Page."""
    reviews = Review.objects.select_related('book', 'user').all()
    return render(request, 'reviews.html', {'reviews': reviews})

def events_view(request):
    """Community Events Page."""
    return render(request, 'events.html')

def faqs_view(request):
    """FAQs Page."""
    return render(request, 'faqs.html')

def book_detail(request, pk):
    """Detailed view of an eBook with review submission and chapter preview."""
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all().select_related('user')
    is_saved = False
    if request.user.is_authenticated:
        is_saved = UserLibrary.objects.filter(user=request.user, book=book).exists()

    review_form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            messages.success(request, "Your review has been published!")
            return redirect('book_detail', pk=book.pk)

    context = {
        'book': book,
        'reviews': reviews,
        'is_saved': is_saved,
        'review_form': review_form,
    }
    return render(request, 'books/book_detail.html', context)

@login_required
def book_create(request):
    """CRUD: Add a new eBook to the catalog."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f"'{book.title}' added successfully!")
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'books/book_create.html', {'form': form, 'title': 'Add New eBook'})

@login_required
def book_delete(request, pk):
    """CRUD: Delete an eBook."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f"'{title}' has been removed from BookSphere.")
        return redirect('home')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

@login_required
def reading_list(request):
    """User's bookmarked reading list."""
    saved_items = UserLibrary.objects.filter(user=request.user).select_related('book', 'book__category')
    return render(request, 'books/reading_list.html', {'saved_items': saved_items})

# ----------------- AUTHENTICATION -----------------

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f"Welcome to BookSphere, {user.username}!")
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

# ----------------- RESTFUL API ENDPOINTS -----------------

def api_books_list(request):
    """RESTful API: List and filter eBooks in JSON."""
    books = Book.objects.all()
    q = request.GET.get('q', '').strip()
    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__icontains=q))
    
    category = request.GET.get('category', '').strip()
    if category:
        books = books.filter(category__slug=category)

    data = [
        {
            'id': b.id,
            'title': b.title,
            'author': b.author,
            'category': b.category.name if b.category else None,
            'publication_year': b.publication_year,
            'pages': b.pages,
            'cover_image_url': b.cover_image_url,
            'average_rating': b.average_rating,
            'review_count': b.review_count,
        }
        for b in books
    ]
    return JsonResponse({'status': 'success', 'count': len(data), 'books': data})

def api_book_detail(request, pk):
    """RESTful API: Get specific book detail."""
    b = get_object_or_404(Book, pk=pk)
    return JsonResponse({
        'status': 'success',
        'book': {
            'id': b.id,
            'title': b.title,
            'author': b.author,
            'category': b.category.name if b.category else None,
            'description': b.description,
            'publication_year': b.publication_year,
            'pages': b.pages,
            'cover_image_url': b.cover_image_url,
            'preview_content': b.preview_content,
            'average_rating': b.average_rating,
            'review_count': b.review_count,
        }
    })

@require_POST
def api_toggle_bookmark(request, pk):
    """RESTful API: Async bookmark toggle."""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Authentication required'}, status=401)

    book = get_object_or_404(Book, pk=pk)
    saved_item = UserLibrary.objects.filter(user=request.user, book=book).first()
    if saved_item:
        saved_item.delete()
        is_saved = False
        msg = f"'{book.title}' removed from your reading list."
    else:
        UserLibrary.objects.create(user=request.user, book=book)
        is_saved = True
        msg = f"'{book.title}' saved to your reading list!"

    return JsonResponse({'status': 'success', 'is_saved': is_saved, 'message': msg})
