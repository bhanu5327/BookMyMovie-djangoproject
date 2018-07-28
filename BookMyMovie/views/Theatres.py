from django.views.generic import ListView, CreateView, UpdateView, DeleteView,View

from BookMyMovie.forms import *
from BookMyMovie.models import *
from django.shortcuts import *
from django.urls import *


from .auth import *
from django.contrib.auth.models import Permission,User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth import logout
raise_exception=True
from django.utils import timezone
import datetime
from datetime import timedelta

class TheatresListView(ListView):

    model = Theatres
    context_object_name = 'Theatres_List'
    template_name = 'TheatreForm.html'
    def get_context_data(self, *, object_list=None, **kwargs):

        context = {}
        context['Theatres_List']=Theatres.objects.all().filter(Location_id=self.kwargs['pk1']).filter(Movie_id=self.kwargs['pk'])
        self.request.session['movie_id'] = self.kwargs['pk']
        self.request.session['theatre_id'] = False
        self.request.session['bookedseats'] = False
        self.request.session['timevalue'] = False
        self.request.session['datevalue'] = False
        self.request.session['payment'] = False
        context['locationid']=self.kwargs['pk1']
        context['movieid']=self.kwargs['pk']
        context.update({'user_permissions':self.request.user.get_all_permissions()})
        k=self.request.META.get('HTTP_REFERER')
        context['startdate']=str(datetime.datetime.now(tz=timezone.utc)).split()[0]
        context['enddate']=str(datetime.datetime.now(tz=timezone.utc)+timedelta(days=7)).split()[0]
        return context
    def post(self,request,*args,**kwargs):
        now = datetime.datetime.now()
        import pytz
        tz = pytz.timezone('Asia/Kolkata')
        your_now = now.astimezone(tz)
        t = str(your_now)
        t = t.split()

        if t[0] == request.POST['date']:
            t = t[1].split(':')
            t = int(t[0])
            t1 = 0
            if request.POST['time'] == "11:00AM":
                t1 = 11
            elif request.POST['time'] == "2:00PM":
                t1 = 14
            elif request.POST['time'] == "6:00PM":
                t1 = 18
            elif request.POST['time'] == "9:00PM":
                t1 = 21
            if t >= t1:
                self.request.session['invalidtime'] = True
                return redirect('BookMyMovieApp:ViewTheatres', pk1=self.request.session['location_id'],
                                pk=self.request.session['movie_id'])
        return redirect('BookMyMovieApp:ViewSeats', pk=request.POST['theatre_id'] ,datevalue=request.POST['date'],timevalue=request.POST['time'])


class CreateTheatreView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):

    login_url = '/login/'
    permission_required = 'BookMyMovieApp.add_Theatres'
    permission_denied_message = 'k8ijuhg'
    raise_exception = True
    model=Theatres
    form_class = TheatreForm
    template_name = 'form.html'

    def post(self, request, *args, **kwargs):

        location=Locations.objects.get(id=self.kwargs['pk1'])
        movie=Movies.objects.get(id=self.kwargs['pk'])

        # import ipdb
        # ipdb.set_trace()
        theatre_form=TheatreForm(request.POST,request.FILES)

        if theatre_form.is_valid():
            theatre=theatre_form.save(commit=False)

            theatre.Location=location
            theatre.Movie=movie
            theatre.save()

        return redirect('BookMyMovieApp:ViewTheatres',pk=self.kwargs['pk'],pk1=self.kwargs['pk1'])

class EditTheatreView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    permission_required = 'BookMyMovieApp.change_Theatres'
    permission_denied_message = 'k8ijuhg'
    raise_exception = True
    model = Theatres
    form_class = TheatreForm
    template_name = 'form.html'

    def post(self, request, *args, **kwargs):

        theatre=Theatres.objects.get(id=self.kwargs['pk'])
        theatre_form=TheatreForm(request.POST,request.FILES,instance=theatre)
        if theatre_form.is_valid():
            theatre=theatre_form.save(commit=True)



        return redirect('BookMyMovieApp:ViewTheatres' ,pk1=self.kwargs['pk2'],pk=self.kwargs['pk1'])


class DeleteTheatreView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/login/'
    permission_required = 'BookMyMovieApp.delete_Theatres'
    permission_denied_message = 'k8ijuhg'
    raise_exception = True
    model = Theatres
    template_name = 'deleteform.html'
    def post(self,request,*args,**kwargs):
        theatre=Theatres.objects.get(id=self.kwargs['pk'])
        theatre.delete()
        return redirect('BookMyMovieApp:ViewTheatres',pk1=self.kwargs['pk2'],pk=self.kwargs['pk1'])





