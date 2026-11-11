from django.test import TestCase, Client
from django.contrib.auth.models import User
from books.models import Book, Category, Review, UserLibrary

class BookSphereModelAndAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(name="AI & Systems", icon="💻")
        self.book = Book.objects.create(
            title="Clean Architecture",
            author="Robert C. Martin",
            category=self.category,
            description="Software architecture rules.",
            publication_year=2017,
            pages=432
        )

    def test_book_creation_and_rating(self):
        self.assertEqual(self.book.title, "Clean Architecture")
        Review.objects.create(user=self.user, book=self.book, rating=5, comment="Great book")
        self.assertEqual(self.book.average_rating, 5.0)
        self.assertEqual(self.book.review_count, 1)

    def test_book_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Clean Architecture")

    def test_api_books_list(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['count'], 1)

    def test_api_bookmark_toggle(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(f'/api/books/{self.book.id}/bookmark/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['is_saved'])
        self.assertTrue(UserLibrary.objects.filter(user=self.user, book=self.book).exists())
