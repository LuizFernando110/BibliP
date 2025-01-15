from django.urls import path
from .views import index,search,details,borrow,borrow_history, login_teacher, user_register

urlpatterns = [
    path('',index,name='index'),
    path('collection/<str:search>',search,name='search'),
    path('collection/details/<int:book_pk>',details,name='details'),
    path('collection/borrow/<int:book_pk>',borrow,name='borrow'),
    path('collection/history/borrow_history',borrow_history,name='borrow_history'),
    path('login',login_teacher,name='login_teacher'), 
    path('register',user_register,name='user_register'),
]