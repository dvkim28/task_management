from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import UserProfileForm


class UserRegistrationView(CreateView):
    model = get_user_model()
    fields = ("username", "email", "password",)
    template_name = "registration/signup.html"

    def get_success_url(self):
        return reverse_lazy(
            "accounts:user-profile-view", kwargs={
                "pk": self.object.pk
            }
        )

    def form_valid(self, form):
        form.instance.password = make_password(form.cleaned_data['password'])
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserUpdateProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "pages/profile.html"
    context_object_name = "user"
    form_class = UserProfileForm

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy(
            "accounts:user-profile-view", kwargs={
                "pk": self.object.pk
            }
        )
