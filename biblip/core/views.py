from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.views.generic import ListView,DetailView,FormView
from .forms import loginTeacherForm, userRegisterForm,SchoolClassForm
from employee.models import Book,Borrow

#importançoes temporararias para o json:
import json
from django.conf import settings
import os
from .forms import loginTeacherForm, userRegisterForm
from employee.models import Book, Borrow, Profile

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
    template_name='employer_borrow_list.html'
    context_object_name='borrow_history'

    def get_queryset(self):
        prof=self.request.user.profile
        queryset=Borrow.objects.filter(borrow_teacher=prof)
        return queryset

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['filter_title']='Histórico de alugueis'
        return context
    


class borrow_details(DetailView):
    template_name="employer_borrow_details.html"
    model=Borrow
    context_object_name='borrow'
    pk_url_kwarg='borrow_pk'

def login_teacher(request):
    context={'form':loginTeacherForm()}
    return render(request,'core/login_teacher.html',context)

def user_register(request):
    context = {'form': userRegisterForm()}
    return render(request, 'core/user_register.html', context)


class school_class_creation(FormView):
    form_class=SchoolClassForm
    template_name='core/class_register_modal.html'
    success_url=reversed('index')

    def form_valid(self, form):
        form.save(profile=self.request.user.profile)
        messages.add_message(self.request,messages.SUCCESS,"Turma adicionada com sucesso")
        return redirect('index')
