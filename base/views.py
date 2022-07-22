from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import auth
from .forms import CustomUserCreationForm, LoginForm
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView,
)
import pdb


from base.models import User

# Create your views here.
class SignupView(CreateView):
    """
    shows the signup form and registers a new user with the given data
    """

    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

    def post(self, *args, **kwargs):
        data = self.request.POST
        form = self.form_class(data)

        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(self.request, self.template_name, status=400)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class LoginPageView(View):
    """
    authenticates the user if credentials are correct else redirects back to login page
    """

    template_name = "registration/login.html"
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ""
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )

    def post(self, request):
        form = self.form_class(request.POST)
        user = auth.authenticate(
            email=self.request.POST.get("email"),
            password=self.request.POST.get("password"),
        )
        if user is not None:
            auth.login(self.request, user)
            return redirect("chat:home")
        return render(request, self.template_name, context={"form": form})


class Logout(View):
    """
    logs the user out
    """

    def dispatch(
        self,
        *args,
        **kwargs,
    ):
        """
        logs the user out
        """
        auth.logout(self.request)
        return redirect("login")


def signup(request):
    if request.method == "POST":
        data = dict(request.POST)
        data.pop("csrfmiddlewaretoken", None)
        data.pop("password1", None)
        data["password"] = (
            data["password2"] if "password2" in data else data["password"]
        )
        data.pop("password2", None)
        data["mobile"] = int(data["mobile"][0])

        data = User.objects.create(**data)
        return redirect("login")
    else:
        return render(
            request, "registration/signup.html", {"form": CustomUserCreationForm()}
        )



