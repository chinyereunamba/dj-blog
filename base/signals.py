from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Check if the user already exists
        if sociallogin.is_existing:
            # Redirect existing users to login
            if request.GET.get("process") == "signup":
                raise ImmediateHttpResponse(HttpResponseRedirect("/accounts/login/"))
