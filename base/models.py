import os
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone

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

    image = models.ImageField(
        _("Profile Image"), upload_to="profile/", default="user.png"
    )

    last_login = models.DateTimeField(
        _("Last Login"), auto_now=True, blank=True)
    date_joined = models.DateField(
        _("Date Joined"), auto_now_add=True, blank=True)

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

    def rename_image(self, filename):
        ext = filename.split(".")[-1]
        new_filename = f"{self.username}.{ext}"
        # Return the path to upload the file
        return os.path.join("profile/", new_filename)

    def save(self, *args, **kwargs):
        if self.image:  # Ensure image exists
            file_path = os.path.join("media", self.image.name)  # Full path

            # If file already exists, delete it before saving the new one
            if os.path.exists(file_path):
                os.remove(file_path)  # Delete existing file

            # Rename the file before saving
            self.image.name = self.rename_image(self.image.name)

        super().save(*args, **kwargs)

    def has_module_perms(self, app_label):
        """
        Check if the user has permissions to view the app.
        This is required for the Django admin interface.
        """
        return True


class Tag(models.Model):
    tag = models.CharField(_("Tag"), max_length=50, unique=True)
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

    user = models.ForeignKey(Account, verbose_name=_(
        "User"), on_delete=models.CASCADE)
    title = models.CharField(_("Post Title"), max_length=255)
    description = models.CharField(_("Excerpt"), max_length=400)
    content = CKEditor5Field(_("Post Content"), config_name="extends")
    featured_image = models.URLField(
        _("Featured Image"), max_length=200, blank=True)
    tags = models.ManyToManyField(
        Tag, verbose_name=_("Tags"), related_name="post")
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    publish_date = models.DateTimeField(_("Published"), blank=True, null=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.title

    def is_published(self):
        return self.status == "published" and (
            self.publish_date is None or self.publish_date <= timezone.now()
        )

    @property
    def read_time(self):
        words_per_minute = 200
        words = len(self.content.split())
        minutes = words / words_per_minute
        read_time = round(minutes)
        return read_time

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1

            # Ensure uniqueness by appending numbers if needed
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def has_permission_to_preview(self, user):
        """
       Check if the given user can preview this blog post.
       The user can preview if they are the author, have staff/admin permissions,
       or belong to a group (e.g., 'Editors') that can preview drafts.
       """
        return (
            self.user == user or # Check if user is the author
            user.is_staff or
            user.is_superuser or
            # Check if user is in 'Editors' group
            user.groups.filter(name='Editors').exists()
        )


class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.TextField(_("Comment"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
