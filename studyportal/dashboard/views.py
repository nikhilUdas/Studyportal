from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import NotesForm, HomeworkForm, DashboardForm, TodoForm
from .models import Notes, Homework, Todo # Ensure Todo is imported
from django.views import generic
from youtubesearchpython import VideosSearch  # Ensure youtubesearchpython is installed and works
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.urls import reverse


# Home View
def home(request):
    return render(request, 'dashboard/home.html')

# Notes View
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            note = Notes(
                user=request.user, 
                title=form.cleaned_data['title'], 
                description=form.cleaned_data['description']
            )
            note.save()
            messages.success(request, f"Notes added by {request.user.username} successfully!")  
            return redirect('notes')  
    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)  # Only show logged-in user's notes
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)

# Delete Note View
def delete_note(request, id):
    note = get_object_or_404(Notes, id=id, user=request.user)  # Ensure user can only delete their own notes
    note.delete()
    messages.success(request, "Note deleted successfully!")
    return redirect('notes')

# Note Detail View
class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = "dashboard/notes_detail.html"
    context_object_name = "note"

# Update Note View
def update_note(request, id):
    note = get_object_or_404(Notes, id=id, user=request.user)  # Ensure user can only update their own notes
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully!")
            return redirect('notes')
    else:
        form = NotesForm(instance=note)
    
    context = {'form': form, 'note': note}
    return render(request, 'dashboard/update_note.html', context)

# Homework View
def homeWork(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.user = request.user
            homework.save()
            messages.success(request, "Homework added successfully!")  
            return redirect('homework')
    else:
        form = HomeworkForm()

    homeworks = Homework.objects.filter(user=request.user)
    context = {'homeworks': homeworks, 'form': form}
    return render(request, 'dashboard/homework.html', context)

# Delete Homework View
def delete_homework(request, id):
    homework = get_object_or_404(Homework, id=id, user=request.user)
    homework.delete()
    messages.success(request, "Homework deleted successfully!")
    return redirect('homework')

# Update Homework (Mark as Complete)
def update_homework(request, id):
    homework = get_object_or_404(Homework, id=id, user=request.user)
    homework.is_finished = not homework.is_finished  # Toggle status
    homework.save()
    return redirect('homework')

# YouTube View (Search form for YouTube)
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']  # Using form.cleaned_data for safety
            video = VideosSearch(text, limit=10)  # Query YouTube API using the search term
            result_list = []

            for i in video.result()['result']:  
                result_dict = {
                    'input': text,
                    'title': i['title'],
                    'duration': i['duration'],
                    'thumbnails': i['thumbnails'][0]['url'],
                    'channel': i['channel']['name'],
                    'link': i['link'],
                    'viewcount': i['viewCount']['short'],
                    'published': i['publishTime'],
                }
                desc = ''
                if i.get("descriptionSnippet"):  # Ensure safe handling of missing description snippet
                    for j in i["descriptionSnippet"]:
                        desc += j['text']
                result_dict['description'] = desc
                result_list.append(result_dict)
            
            context = {'form': form, 'results': result_list}
            return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm()

    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)

# Todo View
def todo(request):
    todos = Todo.objects.filter(user=request.user)  # Fetch tasks for logged-in user

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, "New task added!")
            return redirect('todo')
    else:
        form = TodoForm()

    context = {'todos': todos, 'form': form}
    return render(request, 'dashboard/todo.html', context)

# Toggle is_finished Status
def update_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.is_finished = not todo.is_finished  # Toggle checkbox state
    todo.save()
    return redirect('todo')

# Delete a Task
def delete_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect('todo')


def books(request):
    return render(request, 'dashboard/books.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!") 
            return redirect("login")     
    else:
        form = UserCreationForm()
    return render(request, 'dashboard/register.html', {'form': form})

def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False

    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todos_done': todos_done
    }
    return render(request, 'dashboard/profile.html',context)

def logout_view(request):
    logout(request)
    return render(request, 'dashboard/logout.html')