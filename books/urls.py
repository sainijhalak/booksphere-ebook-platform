from django.urls import path
from . import views

urlpatterns = [
    # Pages from original BookSphere UI
    path('', views.home_view, name='home'),
    path('ebook/', views.ebook_view, name='ebook'),
    path('about/', views.about_view, name='about'),
    path('download/', views.download_view, name='download'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('events/', views.events_view, name='events'),
    path('faqs/', views.faqs_view, name='faqs'),

    # Detail & CRUD operations
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/new/', views.book_create, name='book_create'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('reading-list/', views.reading_list, name='reading_list'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # RESTful API
    path('api/books/', views.api_books_list, name='api_books_list'),
    path('api/books/<int:pk>/', views.api_book_detail, name='api_book_detail'),
    path('api/books/<int:pk>/bookmark/', views.api_toggle_bookmark, name='api_toggle_bookmark'),
]
