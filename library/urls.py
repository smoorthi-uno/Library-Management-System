from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'library'

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),

    # sign up url
    path('register/', views.register, name='register'),

    path('member_list', views.member_list, name='member_list'),
    path('member/create/', views.member_new, name='member_new'),
    path('member/<int:pk>/edit/', views.member_edit, name='member_edit'),
    path('member/<int:pk>/delete/', views.member_delete, name='member_delete'),

    # path('librarian_list', views.librarian_list, name='librarian_list'),
    # path('librarian/<int:pk>/edit/', views.librarian_edit, name='librarian_edit'),
    # path('librarian/<int:pk>/delete/', views.librarian_delete, name='librarian_delete'),

    path('book_list', views.book_list, name='book_list'),
    path('book/create/', views.book_new, name='book_new'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),

    path('genre_list', views.genre_list, name='genre_list'),
    path('genre/create/', views.genre_new, name='genre_new'),
    path('genre/<int:pk>/edit/', views.genre_edit, name='genre_edit'),
    path('genre/<int:pk>/delete/', views.genre_delete, name='genre_delete'),

    path('author_list', views.author_list, name='author_list'),
    path('author/create/', views.author_new, name='author_new'),
    path('author/<int:pk>/edit/', views.author_edit, name='author_edit'),
    path('author/<int:pk>/delete/', views.author_delete, name='author_delete'),

    path('borrow_list', views.borrow_list, name='borrow_list'),
    path('borrow/create/', views.borrow_new, name='borrow_new'),
    path('borrow/<int:pk>/edit/', views.borrow_edit, name='borrow_edit'),
    path('borrow/<int:pk>/delete/', views.borrow_delete, name='borrow_delete'),

    path('pdf/', views.borrow_summary_pdf, name='borrow_summary_pdf'),
]
