from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# Create your models here.


class MyManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if email is None:
            raise ValueError(_("Users must have an email address"))
        if username is None:
            raise ValueError(_("Users must have a username"))

        email = self.normalize_email(email=email).lower()

        user = self.model(email=email, username=username, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        user = self.create_user(
            email=email, username=username, password=password, **extra_fields
        )

        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"), max_length=80, unique=True)
    username = models.CharField(_("Username"), max_length=50, unique=True)
    
    email_verified = models.BooleanField(default=False)

    bio = models.TextField(_("Bio"), blank=True)
    first_name = models.CharField(_("First name"), max_length=50, blank=True)
    last_name = models.CharField(_("Last name"), max_length=50, blank=True)

    last_login = models.DateTimeField(_("Last Login"), auto_now=True, blank=True)
    date_joined = models.DateField(_("Date Joined"), auto_now_add=True, blank=True)

    is_active = models.BooleanField(_("Active"), default=True)
    is_superuser = models.BooleanField(_("Super User"), default=False)
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_admin = models.BooleanField(_("Admin"), default=False)

    objects = MyManager()

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Check if the user has a specific permission."""
        return True

    def has_module_perms(self, app_label):
        """
        Check if the user has permissions to view the app.
        This is required for the Django admin interface.
        """
        return True


class Tag(models.Model):
    tag = models.CharField(_("Tag"), max_length=50)
    created_at = models.DateField(_("Created"), auto_now_add=True)

    def __str__(self):
        return self.tag


class Category(models.Model):
    category = models.CharField(_("Category"), max_length=50)
    created_at = models.DateField(_("Created"), auto_now_add=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Categories"


class BlogPost(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    user = models.ForeignKey(Account, verbose_name=_("User"), on_delete=models.CASCADE)
    title = models.CharField(_("Post Title"), max_length=255)
    description = models.TextField(_("Excerpt"))
    content = models.TextField(_("Post Content"))
    featured_image = models.URLField(_("Featured Image"), max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"), related_name="post")
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)
    slug = models.SlugField(_("Slug"), max_length=255, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.title)

            has_slug = BlogPost.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.title) + "-" + str(count)
                has_slug = BlogPost.objects.filter(slug=slug).exists()

            self.slug = slug

        super().save(*args, **kwargs)
