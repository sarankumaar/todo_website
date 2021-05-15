from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from .models import Task

class Custom(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class Register(FormView):
    template_name='base/register.html'
    form_class = UserCreationForm 
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return super(Register,self).form_valid(form)
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(request, *args, **kwargs)


class Tasklist(LoginRequiredMixin,ListView):
    model= Task
    context_object_name = 'tasks'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search=self.request.GET.get('search')
        if search:
            context['tasks']=context['tasks'].filter(title__icontains=search)or ""
        context['search_value']=search
        return context

class Taskdetail(LoginRequiredMixin,DetailView):
    model = Task
    template_name= 'base/detail_list.html'

class Taskcreate(LoginRequiredMixin,CreateView):
    model = Task
    template_name= 'base/create_list.html'
    fields = ['title','desc','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

class Taskupdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','desc','complete']
    template_name= 'base/create_list.html'
    success_url = reverse_lazy('tasks')
class Taskdelete(LoginRequiredMixin,DeleteView):
    model = Task
    template_name= 'base/delete_list.html'
    success_url = reverse_lazy('tasks')