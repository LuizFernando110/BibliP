from django.urls import path
from .views import borrow_management,delete_book,update_book,create_book,employer_borrow_list,employer_borrow_details

urlpatterns = [
    path('employer/borrow_management',borrow_management,name='borrow_management'),
    path('employer/borrow_management/borrow_list',employer_borrow_list,name='employer_borrow_list'),
    path('employer/borrow_management/employer_borrow_details/<int:borrow_pk>',employer_borrow_details,name='employer_borrow_details'),
    path('employer/create_book',create_book,name='create_book'),
    path('employer/update_book',update_book,name='update_book'),
    path('employer/delete_book',delete_book,name='delete_book'),

]