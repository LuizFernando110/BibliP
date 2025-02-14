from django.shortcuts import render,HttpResponse
#importançoes temporararias para o json:
import json
from django.conf import settings
import os
from django.views.generic import CreateView, FormView
from .forms import SchoolClassForm, ProfileRegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from employee.models import Profile
#arquivos com _temp no final são temporários
#leituras de jsons por agora são temporarias
def index(request):
    json_path_temp = os.path.join(settings.BASE_DIR, 'core', 'books.json') 
    with open (json_path_temp, 'r') as file:
        books = json.load(file)
    return render(request,'core/index.html', {'books': books})

def search(request,search):
    context={'search':search}

    #podemos reutilizar o Index.html nesta rota, mas prtimeiro precisamos da conexão com o banco de dados
    return render(request,"core/search_temp.html",context)


def details(request,book_pk):
    context={'book_pk':book_pk}
    return render(request,'core/book_details.html',context)

def borrow(request,book_pk):
    context={'book_pk':book_pk}
    return render(request,'core/book_borrow.html',context)

def borrow_history(request):
    json_path_temp = os.path.join(settings.BASE_DIR, 'core', 'borrow_history.json') 
    with open (json_path_temp, 'r') as file:
        borrow_history = json.load(file)
    return render(
        request,
        'core/borrow_history.html',
        {
            'filter_title': 'Histórico de alugueis',
            'borrow_history': borrow_history
        }
    )

def borrow_details(request, borrow_pk):
    json_path_temp = os.path.join(settings.BASE_DIR, 'core', 'borrow_history.json') 
    with open (json_path_temp, 'r') as file:
        borrow_history = json.load(file)

    context={'borrow_history': borrow_history}
    return render(request, "employer_borrow_details.html", context)


class ProfileRegistrationCreateView(CreateView):
    form_class = ProfileRegistrationForm
    model = User
    template_name = "core/user_register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        confirm_password = form.cleaned_data.get('confirm_password')

        if password != confirm_password:
            form.add_erro('confirm_password', 'As senhas não são compatíveis.')
            return super().form_invalid(form)
        
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'core/login.html'  
    form_class = LoginForm


    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        remeber_me = form.cleaned_data['remember_me']


        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            if remeber_me:
                self.request.session.set_expiry(2592000)
            else:
                self.request.session.set_expiry(0)
                
            return redirect(self.get_success_url(user))
        else:
            messages.error(self.request, "Usuário ou senha inválidos.")
            return self.form_invalid(form)  

    def get_success_url(self, user):
        try:
            profile = get_object_or_404(Profile, user=user)
            if profile.profile_type == 1:
                return reverse('borrow_management')
            else:
                return reverse('index')
        except Profile.DoesNotExist:
            logout(self.request)
            return reverse('login')
        
    
    def form_invalid(self, form):
        if not form.is_valid():
            messages.error(self.request, "Usuário ou senha incorreto")

        return self.render_to_response(self.get_context_data(form=form))

    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url(request.user))
        return super().dispatch(request, *args, **kwargs)
    

class LogoutView(LogoutView):
    next_page = reverse_lazy('login')


def school_class_creation(request):
    form=SchoolClassForm(request.POST or None,request.FILES or None)
    if request.method=='POST':
        if form.is_valid():
            form.save(profile=request.user.profile)
    return HttpResponse('criado')

def teste(request):
    context = {'form':SchoolClassForm}
    return render(request, 'core/class_register_modal.html', context)