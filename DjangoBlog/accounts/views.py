from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import FormView ,RedirectView
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
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
#is_safe_url在4.0之后被废弃
from django.utils.http import url_has_allowed_host_and_scheme  
import traceback

# Create your views here.
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/registration_form.html'
    print("RegisterView() enter")

    def form_valid(self,form):
        user =form.save(False)
        #traceback.print_stack()
        user.save(True)
        url = reverse('accounts:login')
        return HttpResponseRedirect(url)

class LogoutView(RedirectView):
    url ='/login/'

    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs):
        return super(LogoutView,self).dispatch(request,*args,**kwargs)
    
    def get(self,request,*args,**kwargs):
        from DjangoBlog.utils import cache
        cache.clear()
        logout(request)
        return super(LogoutView,self).get(request,*args,**kwargs)

class LoginView(FormView):
    form_class = LoginForm
    template_name = "account/login.html"
    success_url = '/'
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs):
        return super(LoginView,self).dispatch(request,*args,**kwargs)

    
    def form_valid(self,form):
        form =AuthenticationForm(data=self.request.POST,request=self.request)
        print("登录")
        traceback.print_stack()
        if form.is_valid():
            from DjangoBlog.utils import cache
            if cache and cache is not None:
                cache.clear()
            auth.login(self.request,form.get_user())
            
            return HttpResponseRedirect('/')

        else:
            return self.render_to_response({'form':form})

    def get_success_url(self):
        redirect_to =self.request.GET.get(self.redirectfieldname)
        if not url_has_allowed_host_and_scheme(url=redirect_to,allowed_hosts=[self.request.get_host()]):
            retdirect_to = self.success_url
        
        return redirect_to
