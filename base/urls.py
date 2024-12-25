from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    about,
    activate,
    edit_profile,
    login_view,
    logout_view,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    profile,
    SignupView,
    view_post,
)

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path("login/", login_view, name="login"),
    path("sign-up/", SignupView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("logout/", logout_view, name="logout"),
    path("u/<str:username>/", profile, name="profile"),
    path("u/<str:username>/edit/", edit_profile, name="edit-profile"),
    path("about/", about, name="about"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post"),
    path("add-post/", PostCreateView.as_view(), name="add-post"),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="edit-post"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="delete-post"),
]


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
