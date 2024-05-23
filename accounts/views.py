from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import UserProfileForm
from accounts.models import User


class UserRegistrationView(CreateView):
    model = User
    fields = ("username", "email", "password")
    template_name = "registration/signup.html"

    def get_success_url(self):
        return reverse_lazy(
            "accounts:user-profile-view", kwargs={
                "pk": self.object.pk
            }
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserUpdateProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "pages/profile.html"
    context_object_name = "user"
