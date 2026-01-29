from django.shortcuts import render, redirect, get_object_or_404
from .models import userRegister, todo
from django.contrib import messages

# Helper to get current user
def get_user(request):
    if 'user_id' in request.session:
        return userRegister.objects.get(id=request.session['user_id'])
    return None

def home(request):
    user = get_user(request)
    if not user:
        return redirect('user_login')
    
    # Active todos (not deleted)
    todos = todo.objects.filter(user=user, is_deleted=False).order_by('-created_at')
    return render(request, 'home.html', {'user': user, 'todos': todos, 'page_title': 'My Todos'})

def completed_todos(request):
    user = get_user(request)
    if not user: return redirect('user_login')
    todos = todo.objects.filter(user=user, is_deleted=False, is_completed=True).order_by('-created_at')
    return render(request, 'home.html', {'user': user, 'todos': todos, 'page_title': 'Completed Todos'})

def incomplete_todos(request):
    user = get_user(request)
    if not user: return redirect('user_login')
    todos = todo.objects.filter(user=user, is_deleted=False, is_completed=False).order_by('-created_at')
    return render(request, 'home.html', {'user': user, 'todos': todos, 'page_title': 'Incomplete Todos'})

def deleted_todos(request):
    user = get_user(request)
    if not user: return redirect('user_login')
    todos = todo.objects.filter(user=user, is_deleted=True).order_by('-created_at')
    return render(request, 'home.html', {'user': user, 'todos': todos, 'page_title': 'Recycle Bin', 'is_recycle_bin': True})

def add_todo(request):
    user = get_user(request)
    if not user: return redirect('user_login')
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        todo.objects.create(title=title, description=description, user=user)
        return redirect('home')
    return render(request, 'add_todo.html', {'user': user})

def update_todo(request, id):
    user = get_user(request)
    if not user: return redirect('user_login')
    todo_obj = get_object_or_404(todo, id=id, user=user)
    
    if request.method == 'POST':
        todo_obj.title = request.POST['title']
        todo_obj.description = request.POST['description']
        todo_obj.save()
        return redirect('home')
    return render(request, 'add_todo.html', {'user': user, 'todo': todo_obj, 'is_edit': True})

def delete_todo(request, id):
    user = get_user(request)
    if not user: return redirect('user_login')
    todo_obj = get_object_or_404(todo, id=id, user=user)
    todo_obj.is_deleted = True
    todo_obj.save()
    return redirect('home')

def restore_todo(request, id):
    user = get_user(request)
    if not user: return redirect('user_login')
    todo_obj = get_object_or_404(todo, id=id, user=user)
    todo_obj.is_deleted = False
    todo_obj.save()
    return redirect('deleted_todos')

def permanently_delete_todo(request, id):
    user = get_user(request)
    if not user: return redirect('user_login')
    todo_obj = get_object_or_404(todo, id=id, user=user)
    todo_obj.delete() 
    return redirect('deleted_todos')

def toggle_complete(request, id):
    user = get_user(request)
    if not user: return redirect('user_login')
    todo_obj = get_object_or_404(todo, id=id, user=user)
    todo_obj.is_completed = not todo_obj.is_completed
    todo_obj.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def user_register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        if userRegister.objects.filter(email=email).exists():
           # Should handle error
           pass
        user_image=request.FILES['user_image']
        user=userRegister(username=username,email=email,password=password,user_image=user_image)
        user.save()
        return redirect('user_login')
    return render(request,'user_register.html')

def user_login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        try:
            user=userRegister.objects.get(email=email)
            if user.password==password:
                request.session['user_id'] = user.id
                return redirect('home')
        except userRegister.DoesNotExist:
            pass 
    return render(request,'user_login.html')

def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('user_login')