from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Category, Book, Review

class Command(BaseCommand):
    help = 'Seeds initial categories, sample books, and reviews for BookSphere'

    def handle(self, *args, **options):
        self.stdout.write("Seeding BookSphere database...")

        # Create demo superuser / demo user if not exists
        demo_user, _ = User.objects.get_or_create(
            username="jhalak",
            defaults={"email": "jhalak@example.com", "first_name": "Jhalak", "last_name": "Saini"}
        )
        if not demo_user.has_usable_password():
            demo_user.set_password("demo12345")
            demo_user.is_staff = True
            demo_user.is_superuser = True
            demo_user.save()

        reader_user, _ = User.objects.get_or_create(
            username="reader_alex",
            defaults={"email": "alex@example.com"}
        )
        if not reader_user.has_usable_password():
            reader_user.set_password("reader12345")
            reader_user.save()

        # Categories
        cat_tech, _ = Category.objects.get_or_create(name="Computer Science & AI", defaults={"icon": "💻", "description": "Software architecture, distributed systems, machine learning, and systems engineering."})
        cat_finance, _ = Category.objects.get_or_create(name="Finance & Economics", defaults={"icon": "📈", "description": "Equity valuation, investment principles, quantitative trading, and macroeconomic theory."})
        cat_science, _ = Category.objects.get_or_create(name="Science & Philosophy", defaults={"icon": "🔬", "description": "Physics, biology, cognitive science, and epistemic philosophy."})
        cat_fiction, _ = Category.objects.get_or_create(name="Classic Literature", defaults={"icon": "📖", "description": "Timeless literary masterpieces and foundational storytelling."})

        # Books
        sample_books = [
            {
                "title": "Designing Data-Intensive Applications",
                "author": "Martin Kleppmann",
                "category": cat_tech,
                "description": "The definitive guide to the principles, architectures, and trade-offs of modern distributed databases, stream processors, and storage engines.",
                "publication_year": 2017,
                "isbn": "978-1449373320",
                "pages": 616,
                "cover_image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=500&auto=format&fit=crop&q=60",
                "preview_content": "Chapter 1: Reliable, Scalable, and Maintainable Applications. Data systems today must navigate trade-offs between batch processing, replication lag, and distributed consensus...",
                "is_featured": True
            },
            {
                "title": "Deep Learning: Foundations and Concepts",
                "author": "Christopher M. Bishop & Hugh Bishop",
                "category": cat_tech,
                "description": "Comprehensive mathematical exposition of neural networks, attention mechanisms, diffusion models, and transformer architectures.",
                "publication_year": 2024,
                "isbn": "978-3031454677",
                "pages": 680,
                "cover_image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500&auto=format&fit=crop&q=60",
                "preview_content": "Chapter 1: Linear Regression and Generalization. Machine learning systems seek to identify parameterized functions that minimize empirical risk under regularized inductive priors...",
                "is_featured": True
            },
            {
                "title": "The Intelligent Investor",
                "author": "Benjamin Graham",
                "category": cat_finance,
                "description": "The seminal text on value investing, margin of safety, and emotional discipline in public financial markets.",
                "publication_year": 2003,
                "isbn": "978-0060555665",
                "pages": 640,
                "cover_image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500&auto=format&fit=crop&q=60",
                "preview_content": "Chapter 1: Investment versus Speculation: Results to Be Expected by the Intelligent Investor. An investment operation is one which, upon thorough analysis, promises safety of principal...",
                "is_featured": True
            },
            {
                "title": "Clean Architecture: A Craftsman's Guide to Software Structure",
                "author": "Robert C. Martin",
                "category": cat_tech,
                "description": "Essential architectural rules and boundary discipline for building scalable, testable, and maintainable enterprise software systems.",
                "publication_year": 2017,
                "isbn": "978-0134494166",
                "pages": 432,
                "cover_image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=500&auto=format&fit=crop&q=60",
                "preview_content": "Chapter 1: What is Architecture? The goal of software architecture is to minimize the human resources required to build and maintain the required system...",
                "is_featured": False
            },
            {
                "title": "Principles for Navigating Big Debt Crises",
                "author": "Ray Dalio",
                "category": cat_finance,
                "description": "A template for understanding macro debt cycles, central bank liquidity injections, deleveraging mechanisms, and currency devaluations.",
                "publication_year": 2018,
                "isbn": "978-1732689800",
                "pages": 480,
                "cover_image_url": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=500&auto=format&fit=crop&q=60",
                "preview_content": "Part 1: The Archetypal Debt Cycle. Because one person's spending is another person's income, credit creates economic cycles that must balance productivity growth...",
                "is_featured": True
            },
            {
                "title": "Meditations",
                "author": "Marcus Aurelius",
                "category": cat_science,
                "description": "Timeless reflections on Stoic philosophy, personal discipline, emotional resilience, and ethics written by the Roman emperor.",
                "publication_year": 2002,
                "isbn": "978-0812968255",
                "pages": 256,
                "cover_image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop&q=60",
                "preview_content": "Book 1: Debts and Lessons. From my grandfather Verus, a kindly disposition and sweetness of temper. From my mother, piety and generosity...",
                "is_featured": False
            }
        ]

        for b_data in sample_books:
            book, created = Book.objects.get_or_create(
                title=b_data["title"],
                defaults=b_data
            )
            if created:
                # Add sample reviews
                Review.objects.create(
                    book=book,
                    user=demo_user,
                    rating=5,
                    comment="An absolute masterwork. Critical foundational reading for any systems or financial professional."
                )
                Review.objects.create(
                    book=book,
                    user=reader_user,
                    rating=5,
                    comment="Clear, mathematically rigorous, and exceptionally well articulated."
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(sample_books)} books, categories, and reviews!"))
