from django.shortcuts import render,HttpResponse
#importançoes temporararias para o json:
import json
from django.conf import settings
import os
from .forms import loginTeacherForm, userRegisterForm
from employee.models import Book, Borrow, Profile, Genre
import math

#arquivos com _temp no final são temporários
#leituras de jsons por agora são temporarias

def split_columns(lista):
    num_colls = math.ceil(math.sqrt(len(lista)+1))
    return [lista [i::num_colls] for i in range(num_colls)] 


def index(request):
    genre_id = request.GET.get("genre")

    books = Book.objects.all()
    if genre_id:
        books = books.filter(book_genre__id=genre_id)

    filters = Genre.objects.all()
    todos_filter = Genre(id=None, genre_name="Todos")  # 'Todos' como um filtro sem gênero associado
    filters = [todos_filter] + list(filters)
    filters = split_columns(filters)

    context= {'books': books, 'filters': filters, 'selected_genre': genre_id, 'filter_type': 'genre', 'filter_url':'index'}

    return render(request,'core/index.html', context)

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
    borrow_history = Borrow.objects.filter(borrow_teacher=request.user.profile)
    return render(
        request,
        'core/borrow_history.html',
        {
            'filter_title': 'Histórico de alugueis',
            'borrow_history': borrow_history,
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

def user_register(request):
    context = {'form': userRegisterForm()}
    return render(request, 'core/user_register.html', context)