from django.urls import path
from .views import index,search,details,borrow,borrow_history, borrow_details, ProfileRegistrationCreateView, school_class_creation, teste, LoginView, LogoutView

urlpatterns = [
    path('',index,name='index'),
    path('collection/<str:search>',search,name='search'),
    path('collection/details/<int:book_pk>',details,name='details'),
    path('collection/borrow/<int:book_pk>',borrow,name='borrow'),
    path('collection/history/borrow_history',borrow_history,name='borrow_history'),
    path('collection/history/borrow_history/borrow_details/<int:borrow_pk>',borrow_details,name='borrow_history_details'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register',ProfileRegistrationCreateView.as_view(),name='user_register'),
    path('profile/school_class/create',school_class_creation,name='school_class_creation'),
    path('teste',teste,name='teste'),
]