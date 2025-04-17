from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('notes/', views.notes, name="notes"),
    path('delete-note/<int:id>/', views.delete_note, name="delete-note"),
    path('notes-detail/<int:pk>/', views.NotesDetailView.as_view(), name="notes-detail"),
    path('update-note/<int:id>/', views.update_note, name="update-note"),

    path('homework/', views.homeWork, name="homework"),
    path('delete-homework/<int:id>/', views.delete_homework, name="delete-homework"),
    path('update-homework/<int:id>/', views.update_homework, name="update-homework"),

    path('youtube/', views.youtube, name="youtube"),
    path('todo/', views.todo, name="todo"),
    path('update-todo/<int:id>/', views.update_todo, name="update-todo"),
    path('delete-todo/<int:id>/', views.delete_todo, name="delete-todo"),
    path('books/', views.books, name="books"),
    
]
