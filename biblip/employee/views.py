from django.shortcuts import render,HttpResponse

def borrow_management(request):
    return HttpResponse('<h1>gerenciamento de livros</h1>')

def create_book(request):
    return HttpResponse('<h1>Livro Criado!!</h1>')

def update_book(request):
    return HttpResponse('<h1>Livro Editado</h1>')

def delete_book(request):
    return HttpResponse('<h1>Livro Deletado</h1>')
