from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import RegisterForm,LoginForm
# Create your views here.
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/registation_form.html'

    def form_valid(self,form):
        user =form.save(False)

        user.save(True)
        return HttpResponseRedirect('/')

class LoginView(FormView):
    form_class = LoginForm
    template_name = "account/login.html"
