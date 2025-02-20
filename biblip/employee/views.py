from django.shortcuts import render, HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, View, UpdateView, DeleteView
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from .forms import BookForm
from .models import Book, Borrow, Genre, Author, BookAuthor, BookGenre
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

class borrow_management(ListView):
    model=Borrow
    template_name="employer_index.html"

    def get_context_data(self, **kwargs):
        
        Borrow.objects.annotate(month=ExtractMonth('borrow_delivery_date'))
        today = datetime.today()

        #calculando primeiro e último dia da semana
        #extractWeek usa sehunda como primeiro dia da semana, por isso está sendo feito manualmente
        day_of_week = (datetime.weekday(today)+1)%7 
        first_day_of_the_week=datetime.date(today-timedelta(days=day_of_week))
        last_day_of_the_week=datetime.date(today+timedelta(days=(6-day_of_week)))


        week_appointments=Borrow.objects.filter(borrow_delivery_date__range=(first_day_of_the_week,last_day_of_the_week))
        pending_appointments=Borrow.objects.filter(borrow_status=3)


        appointments_limit = 4
        hidden_week_appointments_count = max(len(week_appointments) - appointments_limit, 0)

        pending_limit = 4
        hidden_pending_count = max(len(pending_appointments) - pending_limit, 0)


        month_appointments=Borrow.objects.filter(borrow_delivery_date__month=ExtractMonth('borrow_delivery_date'))
        month_appointments=month_appointments.exclude(borrow_delivery_date__range=(first_day_of_the_week,last_day_of_the_week))
        hidden_month_appointments_count=max(len(month_appointments) - appointments_limit, 0)

        context = {
            'week_appointments': week_appointments[:appointments_limit], 
            'pending_appointments': pending_appointments[:pending_limit],
            'month_appointments':month_appointments[:appointments_limit],
            'hidden_week_appointments': hidden_week_appointments_count,
            'hidden_month_appointments': hidden_month_appointments_count,
            'hidden_pending': hidden_pending_count,
            'employer': True
        }
        return context

def books_management(request):
    books = Book.objects.all()
    context = {'employer': True, 'books': books}
    return render(request, 'books-management.html', context)

class employer_borrow_list(ListView):
    model=Borrow
    template_name='employer_borrow_list.html'

    def get_context_data(self, **kwargs):
        
        if self.request.method=='GET':
            Borrow.objects.annotate(month=ExtractMonth('borrow_delivery_date'))
            today = datetime.today()

            #calculando primeiro e último dia da semana
            #extractWeek usa sehunda como primeiro dia da semana, por isso está sendo feito manualmente
            day_of_week = (datetime.weekday(today)+1)%7 
            first_day_of_the_week=datetime.date(today-timedelta(days=day_of_week))
            last_day_of_the_week=datetime.date(today+timedelta(days=(6-day_of_week)))


            appointments=Borrow.objects.all()
            if self.request.GET.get('appointments_type')=='month':
                appointments=Borrow.objects.filter(borrow_delivery_date__month=ExtractMonth('borrow_delivery_date'))
                appointments=appointments.exclude(borrow_delivery_date__range=(first_day_of_the_week,last_day_of_the_week))
                
            
            if self.request.GET.get('appointments_type')=='week':
                appointments=Borrow.objects.filter(borrow_delivery_date__range=(first_day_of_the_week,last_day_of_the_week))

        return {'borrow_history':appointments,'employer':True}


class employer_borrow_details(DetailView):
    model=Borrow
    pk_url_kwarg='borrow_pk'  
    template_name='employer_borrow_details.html'
        


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
            for author_id in authors_ids:
                BookAuthor.objects.create(book=book, author_id=author_id)

            # Criando novos autores
            new_authors = request.POST.getlist('new_authors')
            for author_name in new_authors:
                new_author = Author.objects.create(author_name=author_name)
                BookAuthor.objects.create(book=book, author=new_author)

            # Adicionando gêneros existentes
            genre_ids = request.POST.getlist('book_genre')
            for genre_id in genre_ids:
                BookGenre.objects.create(book=book, genre_id=genre_id)

            # Criando novos gêneros
            new_genres = request.POST.getlist('new_genres')
            for genre_name in new_genres:
                new_genre = Genre.objects.create(genre_name=genre_name)
                BookGenre.objects.create(book=book, genre=new_genre)

            return JsonResponse({
                'message': 'Livro criado com sucesso',
                'book_id': book.id,
                'success': True,
                'redirect_url': reverse_lazy("books_management")
            }, status=201)
        else:
            return JsonResponse({"erros": form.errors}, status=400)

class BookEditView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "book_edit.html"
    success_url = reverse_lazy("books_management")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object

        context['employer'] = True
        context['book'] = self.object

        return context
    
    def form_valid(self, form):
        book = form.save(commit=False)
        book.save()

        return super().form_valid(form)
    

class GetBookAssociatedDatas(View):

    def get(self, request, book_id , *args, **kwargs):
        try: 
            book = get_object_or_404(Book, id=book_id)

            genres = BookGenre.objects.filter(book = book)
            genre_data = [{
                'id': genre.genre.id,
                'name': genre.genre.genre_name
            } for genre in genres
            ]

            authors = BookAuthor.objects.filter(book = book)
            author_data = [{
                'id': author.author.id,
                'name': author.author.author_name
            } for author in authors
            ]

            return JsonResponse({
                "genres": genre_data,
                "authors": author_data
            })
        
        except Exception as e:
            print(f"Erro ao buscar dados do livro: {str(e)}")
            return JsonResponse({"error": "Erro interno do servidor"}, status=500)


class UpdateBookAssociatedDatas(View):

    def post(self, request, book_id, *args, **kwargs):
        try:
            book = Book.objects.get(id=book_id)
            form = BookForm(request.POST, request.FILES, instance=book)

            if form.is_valid():
                book = form.save(commit=False)
                book.save()

                # Atualiza os autores
                authors_ids = request.POST.getlist('book_author')
                BookAuthor.objects.filter(book=book).exclude(author_id__in=authors_ids).delete()
                for author_id in authors_ids:
                    BookAuthor.objects.get_or_create(book=book, author_id=author_id)

                new_authors = request.POST.getlist('new_authors')
                new_authors_objs = [Author(author_name=author_name) for author_name in new_authors]
                Author.objects.bulk_create(new_authors_objs, ignore_conflicts=True)
                for new_author in new_authors_objs:
                    BookAuthor.objects.create(book=book, author=new_author)

                # Atualiza os gêneros
                genre_ids = request.POST.getlist('book_genre')
                BookGenre.objects.filter(book=book).exclude(genre_id__in=genre_ids).delete()
                for genre_id in genre_ids:
                    BookGenre.objects.get_or_create(book=book, genre_id=genre_id)

                new_genres = request.POST.getlist('new_genres')
                new_genres_objs = [Genre(genre_name=genre_name) for genre_name in new_genres]
                Genre.objects.bulk_create(new_genres_objs, ignore_conflicts=True)
                for new_genre in new_genres_objs:
                    BookGenre.objects.create(book=book, genre=new_genre)

                return JsonResponse({
                    'message': 'Livro atualizado com sucesso!',
                    'book_id': book.id,
                    'success': True,
                    'redirect_url': reverse_lazy("books_management")
                }, status=200)

            else:
                return JsonResponse({"errors": form.errors}, status=400)

        except Book.DoesNotExist:
            return JsonResponse({"message": "Livro não encontrado.", "success": False}, status=404)

        except Exception as e:
            return JsonResponse({"message": f"Erro: {str(e)}", "success": False}, status=400)


class BookDeleteView(View):

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get('pk')  
        book = get_object_or_404(Book, id=book_id)  # Aqui, pode ser necessário converter para int
        book.delete()
        return JsonResponse({"message": "Livro excluído com sucesso!"}, status=200)