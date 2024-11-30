from django.shortcuts import render,HttpResponse


#arquivos com _temp no final são temporários
def index(request):
    return render(request,'core/index.html')

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
    return HttpResponse('<h1> historico de alugueis</h1>')