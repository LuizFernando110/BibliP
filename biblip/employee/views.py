from django.shortcuts import render, HttpResponse
from django.views.generic.edit import CreateView
#importançoes temporararias para o json:
import json
from django.conf import settings
import os
from .forms import BookForm
from .models import Book, Author, Genre, BookAuthor, BookGenre
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from django.urls import reverse_lazy

def borrow_management(request):
    json_path_temp = os.path.join(settings.BASE_DIR, 'employee', 'appointment.json')
    with open (json_path_temp, 'r') as file:
        appointments = json.load(file)
    #Não esta acontecendo aqui mais a ideia é que o appointments seja os da semana, mas pendencias é entre todos 
    appointments_limit = 8
    hidden_appointments_count = max(len(appointments) - appointments_limit, 0)

    pending_appointments = [app for app in appointments if app.get('pendency')]

    pending_limit = 4
    hidden_pending_count = max(len(pending_appointments) - pending_limit, 0)

    context = {
        'appointments': appointments[:appointments_limit], 
        'pending_appointments': pending_appointments[:pending_limit],
        'hidden_appointments': hidden_appointments_count,
        'hidden_pending': hidden_pending_count,
        'employer': True
    }
    return render(request, 'index.html', context)

def books_management(request):
    books = Book.objects.all()
    context = {'employer': True, 'books': books}
    return render(request, 'books-management.html', context)

def employer_borrow_list(request):
    json_path_temp = os.path.join(settings.BASE_DIR, 'employee', 'appointment.json') 
    with open (json_path_temp, 'r') as file:
        borrow_history = json.load(file)

    context={'employer':True,
             'filter_title': 'Histórico de alugueis',
            'borrow_history': borrow_history}
    return render(request,'employer_borrow_list.html',context)


def employer_borrow_details(request,borrow_pk):
    json_path_temp = os.path.join(settings.BASE_DIR, 'core', 'borrow_history.json') 
    with open (json_path_temp, 'r') as file:
        borrow_history = json.load(file)

    context={'employer':True,
            'borrow_history': borrow_history}
    return render(request,'employer_borrow_details.html',context)


def create_book(request):
    return HttpResponse('<h1>Livro Criado!!</h1>')

def update_book(request):
    return HttpResponse('<h1>Livro Editado</h1>')

def delete_book(request):
    return HttpResponse('<h1>Livro Deletado</h1>')

class BookFormCreateView(CreateView):
    form_class = BookForm
    model = Book
    template_name = "book_register.html"
    context_object_name = 'books'
    success_url = reverse_lazy('books_management')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employer'] = True
        return context
    

class SearchGenreView(ListView):
    model = Genre

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        results = self.model.objects.filter(genre_name__icontains=query)[:5]
        data = {'id': [obj.id for obj in results], 
                'results': [obj.genre_name for obj in results]}
        return JsonResponse(data)

   
class SearchAuthorView(ListView):
    model = Author

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        results = self.model.objects.filter(author_name__icontains=query)[:5]
        data = {'id': [obj.id for obj in results], 
                'results': [obj.author_name for obj in results]}
        return JsonResponse(data)


class BookCreateAjaxView(View):

    def post(self, request, *args, **kwargs):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()

            authors_ids = request.POST.getlist('book_author')
            genre_ids = request.POST.getlist('book_genre')

            for author_id in authors_ids:
                BookAuthor.objects.create(book = book, author_id = author_id)

            for genre_id in genre_ids:
                BookGenre.objects.create(book = book, genre_id = genre_id)

            return JsonResponse({'message': 'Livro criado com sucesso', 
                                 "book_id": book.id,
                                 "success": True,
                                 "redirect_url": reverse_lazy("books_management")}, status=201)
        else:
            return JsonResponse({"erros": form.errors}, status=400)