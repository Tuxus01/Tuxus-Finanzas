from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView, RedirectView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
import Finanzas.settings as setting
from .forms import SignUpForm
#from ..core.models import *




@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')


class LoginFormView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('base:index')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
            
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Iniciar sesión'
        return context

class LogoutRedirectView(RedirectView):
    pattern_name = 'login'
    success_url = reverse_lazy('base:login')
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
    
    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(request)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


