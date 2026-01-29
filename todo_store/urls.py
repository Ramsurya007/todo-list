from django.urls import path
from .views import *

urlpatterns=[
    path('', home, name='home'),
    path('user_register/',user_register,name='user_register'),
    path('user_login/',user_login,name='user_login'),
    path('user_logout/',user_logout,name='user_logout'),
    
    # Todo URLs
    path('add_todo/', add_todo, name='add_todo'),
    path('update_todo/<int:id>/', update_todo, name='update_todo'),
    path('delete_todo/<int:id>/', delete_todo, name='delete_todo'),
    path('restore_todo/<int:id>/', restore_todo, name='restore_todo'),
    path('permanently_delete_todo/<int:id>/', permanently_delete_todo, name='permanently_delete_todo'),
    path('toggle_complete/<int:id>/', toggle_complete, name='toggle_complete'),
    
    # Filtered Views
    path('completed/', completed_todos, name='completed_todos'),
    path('incomplete/', incomplete_todos, name='incomplete_todos'),
    path('deleted/', deleted_todos, name='deleted_todos'),
]