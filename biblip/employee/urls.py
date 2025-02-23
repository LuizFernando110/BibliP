from django.urls import path
from .views import borrow_management, books_management, employer_borrow_list,employer_borrow_details, SearchAuthorView, SearchGenreView ,BookFormCreateView, BookCreateAjaxView, BookEditView, UpdateBookAssociatedDatas, GetBookAssociatedDatas, BookDeleteView
from .ajax_endpoints import accept_borrow,cancel_borrow,student_borrow_deliver,student_borrow_receipt
urlpatterns = [
    path('employer/borrow_management',borrow_management.as_view(),name='borrow_management'),
    path('employer/books_management', books_management.as_view(), name='books_management'),
    path('employer/borrow_management/borrow_list',employer_borrow_list.as_view(),name='employer_borrow_list'),
    path('employer/borrow_management/employer_borrow_details/<int:borrow_pk>',employer_borrow_details.as_view(),name='employer_borrow_details'),
    path('employer/book_register',BookFormCreateView.as_view(),name='book_register'),
    path('search_genre/', SearchGenreView.as_view(), name='search_genre'),
    path('search_author/', SearchAuthorView.as_view(), name='search_author'),
    path('employer/book_edit/<int:pk>', BookEditView.as_view(), name='book_edit'),
    path('book/<int:book_id>/update-associated-datas/', UpdateBookAssociatedDatas.as_view(), name='update_book_associated_data'),
    path('book/<int:book_id>/associated-datas/', GetBookAssociatedDatas.as_view(), name='book_associated_data'),
    path('book/delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),

]

ajax_endpoints=[
    path('book_create_ajax/', BookCreateAjaxView.as_view(), name='book_create_ajax'),
    path('employer/borrow/<int:borrow_pk>/accept_borrow',accept_borrow,name='employer_accept_borrow'),
    path('employer/borrow/<int:borrow_pk>/cancel_borrow',cancel_borrow,name='employer_cancel_borrow'),
    path('employer/borrow/<int:borrow_student_pk>/receipt_borrowstudent',student_borrow_receipt,name='receipt_borrowstudent'),
    path('employer/borrow/<int:borrow_student_pk>/deliver_borrowstudent',student_borrow_deliver,name='deliver_borrowstudent'),
]

urlpatterns+=ajax_endpoints
