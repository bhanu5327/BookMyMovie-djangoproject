from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, DetailView

from BookMyMovie.forms import *
from BookMyMovie.models import *
from django.shortcuts import *
from django.urls import *

from .auth import *
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import logout

raise_exception = True


class UserDetailsView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = UserInfo
    template_name = 'UserForm.html'

    def get_context_data(self, **kwargs):

        context = super(UserDetailsView, self).get_context_data(**kwargs)

        user = User.objects.all().filter(id=self.kwargs['pk'])
        userinfo_list = UserInfo.objects.all().filter(User_id=self.kwargs['pk'])

        context['userdetails'] = user[0]
        context['userinfo_list']=userinfo_list

        return context


class EditUserDetailsView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = UserInfo
    form_class = UserInfoForm

    template_name = 'form.html'


    def get_context_data(self, **kwargs):


        context = super(EditUserDetailsView, self).get_context_data(**kwargs)
        userinfo_form = context.get('userinfo')
        context.update(
            {
            'user_form': UserForm(instance=userinfo_form.User),

            }
        )

        return context
    def post(self, request, *args, **kwargs):

        userinfo=UserInfo.objects.get(id=self.kwargs['pk'])
        userinfo_form=UserInfoForm(request.POST,request.FILES,instance=userinfo)
        user_form=UserForm(request.POST,instance=userinfo.User)

        if userinfo_form.is_valid():
            userinfo_form.save(commit=True)
            if user_form.is_valid():
                user_form.save(commit=True)

        return redirect('BookMyMovieApp:userdetails',pk=userinfo.User_id)


