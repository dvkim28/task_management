from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView


class UserRegistrationView(CreateView):
    model = get_user_model()
    form_class = UserCreationForm
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


class UserUpdateProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "pages/profile.html"
    context_object_name = "user"

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy(
            "accounts:user-profile-view", kwargs={
                "pk": self.object.pk
            }
        )
