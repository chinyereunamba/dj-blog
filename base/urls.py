from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    about,
    activate,
    login_view,
    logout_view,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    preview_post,
    profile,
    SignupView,
    UserLoginView,
    UserProfileUpdateView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    # Auth urls
    path("login/", UserLoginView.as_view(), name="login"),
    path("sign-up/", SignupView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("logout/", logout_view, name="logout"),
    # User profile urls
    path("u/<str:username>/", profile, name="profile"),
    path(
        "u/<str:username>/edit/", UserProfileUpdateView.as_view(), name="edit_profile"
    ),
    path("about/", about, name="about"),
    # Post method urls
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post"),
    path("add-post/", PostCreateView.as_view(), name="add_post"),
    path("post/<slug:slug>/edit/", PostUpdateView.as_view(), name="edit_post"),
    path("post/<slug:slug>/delete/", PostDeleteView.as_view(), name="delete_post"),
    path("post/<slug:slug>/preview/", preview_post, name="preview_post"),
    # Comment method urls
    # path("post/<slug:slug>/", CommentCreateView.as_view(), name="comment"),
]


# Password urls
urlpatterns += [
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change_done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
