from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_list, name='create_list'),
    path('list/<int:list_id>/', views.view_list, name='view_list'),
    path('select_movies/<int:list_id>/', views.select_movies, name='select_movies'),
    path('delete-movies/<int:list_id>/', views.delete_movies, name='delete_movies'),
    path('delete-list/<int:list_id>/', views.delete_list, name='delete_list'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search_movies, name='search_movies'),
    path('my_lists/', views.my_lists, name='my_lists'),
    path('add_to_list/<int:list_id>/', views.add_to_list, name='add_to_list'),
    path('get-public-lists/', views.get_public_lists, name='get_public_lists'),
    path('copy-list/', views.copy_list, name='copy_list'),
]
