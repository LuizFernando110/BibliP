from django.shortcuts import render,HttpResponse
#importançoes temporararias para o json:
import json
from django.conf import settings
import os
from django.views.generic import CreateView 
from .forms import loginTeacherForm, SchoolClassForm, ProfileRegistrationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
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

def login_teacher(request):
    context={'form':loginTeacherForm()}
    return render(request,'core/login_teacher.html',context)

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

def school_class_creation(request):
    form=SchoolClassForm(request.POST or None,request.FILES or None)
    if request.method=='POST':
        if form.is_valid():
            form.save(profile=request.user.profile)
    return HttpResponse('criado')

def teste(request):
    context = {'form':SchoolClassForm}
    return render(request, 'core/class_register_modal.html', context)