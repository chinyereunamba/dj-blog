from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Account, BlogPost, Category, Comment, Tag

# Register your models here.


class AccountAdmin(UserAdmin):

    list_display = (
        "email",
        "username",
        "is_admin",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_admin",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    search_fields = ("email", "username")
    ordering = ("email",)

    fieldsets = (
        ("Basic Info", {"fields": ("email", "username", "first_name", "last_name")}),
        (
            "Groups and Permissions",
            {"fields": ("groups", "user_permissions")},
        ),
        (
            "Permissions",
            {"fields": ("is_admin", "is_superuser", "is_staff", "is_active")},
        ),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        ("Basic Info", {"fields": ("email", "username")}),
        ("Password", {"fields": ("password1", "password2")}),
        (
            "Permissions",
            {"fields": ("is_admin", "is_superuser", "is_staff", "is_active")},
        ),
    )

    readonly_fields = ("last_login",)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "category", "status", "created_at", "updated_at"]
    list_filter = ["status", "category", "created_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"title": ("title",)}  # Optional for auto-slug generation


class TagAdmin(admin.ModelAdmin):
    list_display = ["tag", "created_at"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category", "created_at"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]


admin.site.register(Account, AccountAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
