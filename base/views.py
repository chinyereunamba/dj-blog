from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.views.generic import (
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
)
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .forms import NewUserForm, PostForm, ProfileForm, SearchForm
from .models import Account, BlogPost, Tag

# Create your views here.


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user=user)
            messages.success(request, "Logged in successfully")
            return redirect("profile", request.user.username)
        else:
            messages.error(request, "Username or password incorrect")
    return render(request, "base/login.html")


class SignupView(CreateView):
    template_name = "base/register.html"
    form_class = NewUserForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account until email is verified
        user.save()

        # Generate activation token
        current_site = get_current_site(self.request)
        mail_subject = "Activate your account"
        message = render_to_string(
            "base/activation_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            },
        )
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

        return HttpResponse("Check your email to activate your account.")

    def get_success_url(self):
        return reverse("login")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        login(request, user)
        return HttpResponse("Your account has been activated.")
    else:
        return HttpResponse("Activation link is invalid!")


def logout_view(request):
    logout(request)
    return redirect("home")


def profile(request, username):
    user = get_object_or_404(Account, username=username)
    post = BlogPost.objects.filter(user=user)
    context = {"posts": post, "user": user}
    return render(request, "base/profile.html", context)


def edit_profile(request, username):
    user = get_object_or_404(Account, username=username)
    form = ProfileForm(instance=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", username=username)

    context = {"form": form}
    return render(request, "base/form.html", context)


def about(request):
    return render(request, "base/about.html")


def view_post(request, pk):
    post = BlogPost.objects.get(id=pk)
    context = {"post": post}
    return render(request, "base/post.html", context)


def add_post(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            form.save()
            return redirect("profile", username=request.user.username)
    context = {"form": form}

    return render(request, "base/form.html", context)


class PostDetailView(DetailView):
    model = BlogPost
    template_name = "base/post.html"
    context_object_name = "post"

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})


class PostListView(ListView):
    model = BlogPost
    template_name = "base/index.html"
    context_object_name = "posts"
    ordering = ("title",)
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        tags = self.request.GET.getlist("tag")
        status = self.request.GET.get("status", "published")
        queryset = (
            BlogPost.objects.prefetch_related("tags")
            .filter(status=status)
            .order_by("-created_at")
        )
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

        # Filter by tag
        if tags:
            for tag in tags:
                queryset = queryset.filter(tags__tag__icontains=tag)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_post"] = BlogPost.objects.filter(status="published").order_by(
            "-created_at"
        )[:3]
        context["tags"] = Tag.objects.all()
        context["query"] = self.request.GET.get("query", "")
        context["tag_filter"] = self.request.GET.get("tag", "")  # Added

        return context

    def render_to_response(self, context, **response_kwargs):
        # Handle HTMX requests to render partial HTML
        if self.request.headers.get("HX-Request"):
            return render(self.request, "base/partials/post_list.html", context)
        return super().render_to_response(context, **response_kwargs)


class PostFilterView(ListView):
    model = BlogPost
    template_name = "base/partials/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        # Filter by tag dynamically
        tag_filter = self.request.GET.get("tag")
        queryset = BlogPost.objects.filter(status="published")

        if tag_filter:
            queryset = queryset.filter(tags__name__icontains=tag_filter)

        return queryset


class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = PostForm
    template_name = "base/add-post.html"
    login_url = "/login/"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()

        if "save_draft" in self.request.POST:  # If "Save as Draft" button is clicked
            post.status = "draft"
        elif "publish" in self.request.POST:  # If "Publish" button is clicked
            post.status = "published"

        tags_input = self.request.POST.get("tags", "")  # Get tags from hidden input
        tag_list = [
            tag.strip() for tag in tags_input.split(",") if tag.strip()
        ]  # Clean tags

        for tag_name in tag_list:
            tag, created = Tag.objects.get_or_create(tag=tag_name)
            post.tags.add(tag)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile", kwargs={"username": self.request.user.username})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = PostForm
    template_name = "base/edit-post.html"
    login_url = "/login/"

    def get_object(self):
        return get_object_or_404(BlogPost, id=self.kwargs["pk"], user=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        # Process the tags submitted with the form
        tag_names = self.request.POST.get("tags", "").split(
            ","
        )  # Get the tags from the hidden input
        tags = []
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:  # Only add non-empty tag names
                tag, created = Tag.objects.get_or_create(tag=tag_name)
                tags.append(tag)

        # Clear existing tags and set the new ones
        post.tags.set(tags)
        post.save()

        # Optionally, handle saving as draft or publish status
        if self.request.POST.get("save_draft"):
            post.status = "draft"
            post.save()
        elif self.request.POST.get("publish"):
            post.status = "published"
            post.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile", kwargs={"username": self.request.user.username})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = "base/delete.html"
    success_url = reverse_lazy("profile")
    login_url = "/login/"
