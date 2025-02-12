from django.shortcuts import render,HttpResponse
from django.views.generic import ListView,DetailView
from .forms import loginTeacherForm, userRegisterForm,SchoolClassForm
from employee.models import Book,Borrow

#importançoes temporararias para o json:
import json
from django.conf import settings
import os


#arquivos com _temp no final são temporários
#leituras de jsons por agora são temporarias

class index(ListView):
    model=Book
    context_object_name='books'
    template_name='core/index.html'

    def get_queryset(self):
        search=self.request.GET.get('search')
        if search:
            queryset=Book.objects.filter(book_title__icontains=search)
            return queryset
        queryset=super().get_queryset()
        return queryset

def search(request,search):
    context={'search':search}

    #podemos reutilizar o Index.html nesta rota, mas prtimeiro precisamos da conexão com o banco de dados
    return render(request,"core/search_temp.html",context)



class details(DetailView):
    model=Book
    template_name='core/book_details.html'
    pk_url_kwarg='book_pk'
    context_object_name='book'

def borrow(request,book_pk):
    context={'book_pk':book_pk}
    return render(request,'core/book_borrow.html',context)


class borrow_history(ListView):
    model=Borrow
    template_name='core/borrow_history.html'
    context_object_name='borrow_history'

    def get_queryset(self):
        prof=self.request.user.profile
        queryset=Borrow.objects.filter(borrow_teacher=prof)
        return queryset

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['filter_title']='Histórico de alugueis'
        return context
    

def borrow_details(request, borrow_pk):
    json_path_temp = os.path.join(settings.BASE_DIR, 'core', 'borrow_history.json') 
    with open (json_path_temp, 'r') as file:
        borrow_history = json.load(file)

    context={'borrow_history': borrow_history}
    return render(request, "employer_borrow_details.html", context)

def login_teacher(request):
    context={'form':loginTeacherForm()}
    return render(request,'core/login_teacher.html',context)

def user_register(request):
    context = {'form': userRegisterForm()}
    return render(request, 'core/user_register.html', context)

def school_class_creation(request):
    form=SchoolClassForm(request.POST or None,request.FILES or None)
    if request.method=='POST':
        if form.is_valid():
            form.save(profile=request.user.profile)
    return render(request,'core/class_register_modal.html',{'form':form})

def teste(request):
    context = {'form':SchoolClassForm}
    return render(request, 'core/class_register_modal.html', context)