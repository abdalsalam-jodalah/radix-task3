# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# from django.utils.crypto import get_random_string

# class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
#     def populate_user(self, request, sociallogin, data):
#         user = super().populate_user(request, sociallogin, data)
#         if not user.username:  # empty username
#             user.username = f"user_{get_random_string(8)}"
#         return user
