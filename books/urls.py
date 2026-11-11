from django.urls import path
from . import views

urlpatterns = [
    # Web views
    path('', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/new/', views.book_create, name='book_create'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('reading-list/', views.reading_list, name='reading_list'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # RESTful API
    path('api/books/', views.api_books_list, name='api_books_list'),
    path('api/books/<int:pk>/', views.api_book_detail, name='api_book_detail'),
    path('api/books/<int:pk>/bookmark/', views.api_toggle_bookmark, name='api_toggle_bookmark'),
]
