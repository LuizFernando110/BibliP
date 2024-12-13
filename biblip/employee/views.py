from django.shortcuts import render,HttpResponse

def borrow_management(request):
    return render(request, 'index.html')

def create_book(request):
    return HttpResponse('<h1>Livro Criado!!</h1>')

def update_book(request):
    return HttpResponse('<h1>Livro Editado</h1>')

def delete_book(request):
    return HttpResponse('<h1>Livro Deletado</h1>')
