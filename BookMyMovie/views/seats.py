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



class SeatsListView(ListView):
    login_url='/login/'
    model = SeatsInfo


    context_object_name = 'Seats_List'
    template_name = 'SeatsForm.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(SeatsListView,self).get_context_data(**kwargs)
        context['theatreid']=self.kwargs['pk']
        self.request.session['theatre_id'] = self.kwargs['pk']
        self.request.session['bookedseats'] = False
        self.request.session['timevalue'] = self.kwargs['timevalue']
        self.request.session['datevalue'] = self.kwargs['datevalue']
        self.request.session['movieinfo'] = False
        self.request.session['payment'] = False
        columnslist=[str(i) for i in range(1,11)]
        context['cols']=columnslist
        rowslist=['A','B','C','D','E','F']

        seatslist=[]
        for i in rowslist:
            l=[]
            for j in columnslist:
                l.append(i+str(j))
            seatslist.append(l)

        context['seatslist'] = seatslist
        list2=SeatsInfo.objects.values("SeatNumber").filter(Theatre_id=self.kwargs['pk']).filter(MovieDate=self.kwargs['datevalue']).filter(MovieTime=self.kwargs['timevalue'])
        seatsbookedlist=[i['SeatNumber'] for i in list2]
        context['seatsbookedlist']=seatsbookedlist
        context['timevalue']=self.kwargs['timevalue']
        context['datevalue']=self.kwargs['datevalue']

        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context
    def post(self,request,*args,**kwargs):

        index=0
        theatre=Theatres.objects.get(id=self.kwargs['pk'])

        if request.user.is_anonymous:
            return redirect('BookMyMovieApp:LoginNeeded', timevalue=self.kwargs['timevalue'],
                            datevalue=self.kwargs['datevalue'], pk1=self.kwargs['pk'], pk=request.POST['paycost'],
                            bookedseats=request.POST['allseats'],log="log")
        else:
            while(request.POST['allseats'][index:index+2]!=''):
                seat=SeatsInfo(SeatNumber=request.POST['allseats'][index:index+2],SeatCost=100,MovieDate=self.kwargs['datevalue'],
                              MovieTime=self.kwargs['timevalue'], BookedDateTime=str(datetime.datetime.now(tz=timezone.utc)))
                seat.Theatre=theatre
                seat.User=request.user
                seat.save()
                index=index+2


            return redirect('BookMyMovieApp:BookingSummary',timevalue=self.kwargs['timevalue'],datevalue=self.kwargs['datevalue'], pk1=self.kwargs['pk'],pk=request.POST['paycost'],bookedseats=request.POST['allseats'])
