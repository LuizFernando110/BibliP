from django.urls import path
from .views import borrow_management, books_management, delete_book,update_book,create_book, employer_borrow_list,employer_borrow_details, SearchAuthorView, SearchGenreView ,BookFormCreateView, BookCreateAjaxView

urlpatterns = [
    path('employer/borrow_management',borrow_management.as_view(),name='borrow_management'),
    path('employer/books_management', books_management, name='books_management'),
    path('employer/borrow_management/borrow_list/<str:appointments_type>',employer_borrow_list.as_view(),name='employer_borrow_list'),
    path('employer/borrow_management/employer_borrow_details/<int:borrow_pk>',employer_borrow_details.as_view(),name='employer_borrow_details'),
    path('employer/create_book',create_book,name='create_book'),
    path('employer/update_book',update_book,name='update_book'),
    path('employer/delete_book',delete_book,name='delete_book'),
    path('employer/book_register',BookFormCreateView.as_view(),name='book_register'),
    path('search_genre/', SearchGenreView.as_view(), name='search_genre'),
    path('search_author/', SearchAuthorView.as_view(), name='search_author'),
    path('book_create_ajax/', BookCreateAjaxView.as_view(), name='book_create_ajax'),
]