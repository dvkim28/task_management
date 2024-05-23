from django.urls import path

from accounts.views import UserRegistrationView, UserUpdateProfileView

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/<int:pk>/', UserUpdateProfileView.as_view(),
         name='user-profile-view'),
]
