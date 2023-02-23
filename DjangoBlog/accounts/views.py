from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import RegisterForm,LoginForm
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth from authenticate
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
    
    def form_valid(self,form):
        form =AuthenticationForm(data=self.request.POST,request=self.request)

        if form.is_valid():
            auth.login(self.requst,form.get_user())
            
            return HttpResponseRedirect('/')

        else:
            return self.render_to_response({'form':form})

