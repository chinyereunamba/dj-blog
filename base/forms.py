from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Account, BlogPost, Category, Comment, Tag

from django_ckeditor_5.widgets import CKEditor5Widget


class NewUserForm(UserCreationForm):

    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "bio",
            "password1",
            "password2",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "John",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Doe",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "johndoe@mail.com",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "johndoe",
                }
            ),
            "password1": forms.PasswordInput(
                attrs={
                    "class": "input input-bordered w-full grow",
                    "placeholder": "Enter password",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "class": "input input-bordered w-full grow",
                    "placeholder": "........",
                }
            ),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["bio", "first_name", "last_name", "image"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter your first name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter your last name",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered h-10",
                    "placeholder": "A brief description of yourself",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "file-input file-input-bordered w-full",  # DaisyUI Classes
                    "placeholder": "Upload an image of yourself",
                    "accept": "image/*",
                    "type": "file",
                }
            ),
        }


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = BlogPost
        fields = ["title", "description", "category", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter post title",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "input input-bordered !h-24",
                    "placeholder": "Enter a brief excerpt of your post",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "input select select-bordered rounded-lg",
                }
            ),
            "featured_image": forms.ClearableFileInput(
                attrs={"class": "file-input file-input-bordered w-full"}
            ),
            "publish": forms.CheckboxInput(attrs={"class": "toggle toggle-primary"}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=200, required=False)
    tag = forms.CharField(max_length=100, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered h-24",
                    "placeholder": "Write your comment here",
                }
            ),
        }
