from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tag, Category, BlogPost
from django.db.utils import IntegrityError

class AccountModelTests(TestCase):
    def test_create_user(self):
        """Test creating a user with email and password"""
        email = "testuser@example.com"
        username = "testuser"
        password = "testpassword"
        user = get_user_model().objects.create_user(
            email=email, username=username, password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser"""
        email = "admin@example.com"
        username = "admin"
        password = "adminpassword"
        superuser = get_user_model().objects.create_superuser(
            email=email, username=username, password=password
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_user_without_email(self):
        """Test that creating a user without email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None, username="user", password="password"
            )

    def test_user_without_username(self):
        """Test that creating a user without a username raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email="user@example.com", username=None, password="password"
            )


class TagModelTests(TestCase):
    def test_create_tag(self):
        """Test creating a tag"""
        tag = Tag.objects.create(tag="Technology")
        self.assertEqual(str(tag), "Technology")

    def test_tag_unique(self):
        """Test that tags are unique"""
        Tag.objects.create(tag="Health")
        with self.assertRaises(IntegrityError):
            Tag.objects.create(tag="Health")


class CategoryModelTests(TestCase):
    def test_create_category(self):
        """Test creating a category"""
        category = Category.objects.create(category="Programming")
        self.assertEqual(str(category), "Programming")

    def test_category_plural_meta(self):
        """Test that category has the correct plural name"""
        category = Category.objects.create(category="Science")
        self.assertEqual(str(category._meta.verbose_name_plural), "Categories")


class BlogPostModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", username="testuser", password="testpassword"
        )
        self.category = Category.objects.create(category="Tech")
        self.tag = Tag.objects.create(tag="AI")
    
    def test_create_blog_post(self):
        """Test creating a blog post"""
        post = BlogPost.objects.create(
            user=self.user,
            title="AI Innovations",
            description="The future of AI",
            content="AI is evolving rapidly.",
            category=self.category
        )
        self.assertEqual(str(post), "AI Innovations")
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.category, self.category)
    
    def test_blog_post_slug_creation(self):
        """Test that the slug is created automatically"""
        post = BlogPost.objects.create(
            user=self.user,
            title="AI Innovations",
            description="The future of AI",
            content="AI is evolving rapidly."
        )
        self.assertTrue(post.slug)  # Slug should not be empty
        self.assertNotEqual(post.slug, 'ai-is-evolving-rapidly')

    def test_slug_uniqueness_on_save(self):
        """Test that the slug is unique"""
        BlogPost.objects.create(
            user=self.user,
            title="AI Innovations",
            description="The future of AI",
            content="AI is evolving rapidly."
        )
        post2 = BlogPost.objects.create(
            user=self.user,
            title="AI Innovations",
            description="Another post about AI",
            content="AI is evolving rapidly in different fields."
        )
        self.assertNotEqual(post2.slug, "ai-innovations")  # Should have a unique slug
    
    def test_blog_post_with_tags(self):
        """Test adding tags to a blog post"""
        post = BlogPost.objects.create(
            user=self.user,
            title="AI Innovations",
            description="The future of AI",
            content="AI is evolving rapidly.",
            category=self.category
        )
        post.tags.add(self.tag)
        self.assertIn(self.tag, post.tags.all())

    def test_blog_post_with_status(self):
        """Test setting the status of a blog post"""
        post = BlogPost.objects.create(
            user=self.user,
            title="AI Innovations",
            description="The future of AI",
            content="AI is evolving rapidly.",
            category=self.category,
            status="published"
        )
        self.assertEqual(post.status, "published")

