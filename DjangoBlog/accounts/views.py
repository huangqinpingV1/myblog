from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import RegisterForm,LoginForm
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
import traceback

# Create your views here.
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/registration_form.html'
    print("RegisterView() enter")

    def form_valid(self,form):
        user =form.save(False)
        print("form_valid() enter")
        #traceback.print_stack()
        user.save(True)
        url = reverse('accounts:login')
        print("url="+url)
        return HttpResponseRedirect(url)

@never_cache
def LogOut(requests):
    print("登出")
    trackback.print_stack()
    logout(request=requests,next_page='/index')
    #return redirect('index')
    return HttpResponseRedirect('/')


class LoginView(FormView):
    form_class = LoginForm
    template_name = "account/login.html"
    
    def form_valid(self,form):
        form =AuthenticationForm(data=self.request.POST,request=self.request)
        print("登录")
        traceback.print_stack()
        if form.is_valid():
            auth.login(self.request,form.get_user())
            
            return HttpResponseRedirect('/')

        else:
            return self.render_to_response({'form':form})

