from django.urls import path
from . import views
from .views import Tasklist, Taskdetail, Taskcreate,Taskupdate,Taskdelete,Custom, Register
from django.contrib.auth.views import LogoutView


urlpatterns=[
    path('login/', Custom.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', Register.as_view(),name='register'),
    path('',Tasklist.as_view(),name='tasks'),
    path('task/<int:pk>/',Taskdetail.as_view(),name='detail'),
    path('create/',Taskcreate.as_view(),name='create'),
    path('update/<int:pk>/',Taskupdate.as_view(),name='update'),
    path('delete/<int:pk>/',Taskdelete.as_view(),name='delete'),
]