from django.shortcuts import render,HttpResponse
#importançoes temporararias para o json:
import json
from django.conf import settings
import os

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
    return render(request,'core/index.html',{'filter_tittle':'Histórico'})