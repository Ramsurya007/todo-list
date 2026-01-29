from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import userRegister, todo


# -----------------------------
# Helper: get logged-in user
# -----------------------------
def get_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return userRegister.objects.get(id=user_id)
        except userRegister.DoesNotExist:
            return None
    return None


# -----------------------------
# Home
# -----------------------------
def home(request):
    user = get_user(request)
    if not user:
        return redirect('user_login')

    todos = todo.objects.filter(
        user=user,
        is_deleted=False
    ).order_by('-created_at')

    return render(request, 'home.html', {
        'user': user,
        'todos': todos,
        'page_title': 'My Todos'
    })


# -----------------------------
# Todo Filters
# -----------------------------
def completed_todos(request):
    user = get_user(request)
    if not user:
        return redirect('user_login')

    todos = todo.objects.filter(
        user=user,
        is_deleted=False,
        is_completed=True
    ).order_by('-created_at')

    return render(request, 'home.html', {
        'user': user,
        'todos': todos,
        'page_title': 'Completed Todos'
    })


def incomplete_todos(request):
    user = get_user(request)
    if not user:
        return redirect('user_login')

    todos = todo.objects.filter(
        user=user,
        is_deleted=False,
        is_completed=False
    ).order_by('-created_at')

    return render(request, 'home.html', {
        'user': user,
        'todos': todos,
        'page_title': 'Incomplete Todos'
    })


def deleted_todos(request):
    user = get_user(request)
    if not user:
        return redirect('user_login')

    todos = todo.objects.filter(
        user=user,
        is_deleted=True
    ).order_by('-created_at')

    return render(request, 'home.html', {
        'user': user,
        'todos': todos,
        'page_title': 'Recycle Bin',
        'is_recycle_bin': True
    })


# -----------------------------
# Add / Update Todo
# -----------------------------
def add_todo(request):
    user = get_user(request)
    if not user:
        return redirect('user_login')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        todo.objects.create(
            title=title,
            description=description,
            user=user
        )
        return redirect('home')

    return render(request, 'add_todo.html', {'user': user})


def update_todo(request, id):
    user = get_user(request)
    if not user:
        return redirect('user_login')

    todo_obj = get_object_or_404(todo, id=id, user=user)

    if request.method == 'POST':
        todo_obj.title = request.POST.get('title')
        todo_obj.description = request.POST.get('description')
        todo_obj.save()
        return redirect('home')

    return render(request, 'add_todo.html', {
        'user': user,
        'todo': todo_obj,
        'is_edit': True
    })


# -----------------------------
# Todo Actions
# -----------------------------
def delete_todo(request, id):
    user = get_user(request)
    if not user:
        return redirect('user_login')

    todo_obj = get_object_or_404(todo, id=id, user=user)
    todo_obj.is_deleted = True
    todo_obj.save()
    return redirect('home')


def restore_todo(request, id):
    user = get_user(request)
    if not user:
        return redirect('user_login')

    todo_obj = get_object_or_404(todo, id=id, user=user)
    todo_obj.is_deleted = False
    todo_obj.save()
    return redirect('deleted_todos')


def permanently_delete_todo(request, id):
    user = get_user(request)
    if not user:
        return redirect('user_login')

    todo_obj = get_object_or_404(todo, id=id, user=user)
    todo_obj.delete()
    return redirect('deleted_todos')


def toggle_complete(request, id):
    user = get_user(request)
    if not user:
        return redirect('user_login')

    todo_obj = get_object_or_404(todo, id=id, user=user)
    todo_obj.is_completed = not todo_obj.is_completed
    todo_obj.save()

    return redirect(request.META.get('HTTP_REFERER', 'home'))


# -----------------------------
# User Register
# -----------------------------
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_image = request.FILES.get('user_image')

        if userRegister.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('user_register')

        user = userRegister.objects.create(
            username=username,
            email=email,
            password=password,  # ⚠️ plain text (ok for learning)
            user_image=user_image
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('user_login')

    return render(request, 'user_register.html')


# -----------------------------
# User Login (FIXED)
# -----------------------------
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = userRegister.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            return redirect('home')
        except userRegister.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('user_login')

    return render(request, 'user_login.html')


# -----------------------------
# User Logout
# -----------------------------
def user_logout(request):
    request.session.flush()
    return redirect('user_login')
