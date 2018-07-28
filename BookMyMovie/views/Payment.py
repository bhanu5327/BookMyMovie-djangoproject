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
import datetime
import string
from django.utils import timezone

def LoginNeeded(request,pk1,pk,bookedseats,timevalue,datevalue,log):
    request.session['pk1']=pk1
    request.session['pk']=pk
    request.session['bookedseats']=bookedseats
    request.session['timevalue']=timevalue
    request.session['datevalue']=datevalue
    return  redirect('BookMyMovieApp:login_html')

def JustLogged(request):
    pk=request.session['pk']
    pk1=request.session['pk1']
    bookedseats=request.session['bookedseats']
    datevalue=request.session['datevalue']
    timevalue=request.session['timevalue']

    return redirect('BookMyMovieApp:BookingSummary', timevalue=timevalue,
                    datevalue=datevalue, pk1=pk1, pk=pk,
                    bookedseats=bookedseats)

def BookingSummaryView(request,pk1,pk,bookedseats,timevalue,datevalue):
    dict = {}

    theatre= Theatres.objects.all().filter(id=pk1)
    dict['theatreinfo']=theatre[0]
    dict['theatreid'] = pk1
    dict['paycost'] = pk
    dict['timevalue']=timevalue



    dict['datevalue']=datevalue
    dict['bookedseats']=bookedseats
    request.session['bookedseats']=bookedseats
    request.session['cost']=pk
    return render(request, 'BookingSummary.html', context=dict)

from django.template.loader import render_to_string, get_template
from django.core.mail.message import EmailMultiAlternatives

def CreditcardView(request):
    if(request.session['payment']):
        return render(request,template_name='seatsalreadybooked.html',context={})
    else:
        bookedseats = request.session['bookedseats']
        datevalue = request.session['datevalue']
        timevalue = request.session['timevalue']
        index = 0
        theatre = Theatres.objects.get(id=request.session['theatre_id'])

        s1=bookedseats.split(',')
        k=0
        while (k<len(s1)):

            seat = SeatsInfo(SeatNumber=s1[k], SeatCost=100,
                             MovieDate=datevalue,
                             MovieTime=timevalue, BookedDateTime=str(datetime.datetime.now(tz=timezone.utc)))
            seat.Theatre = theatre
            seat.User = request.user
            seat.save()
            k+=1
        dict={}
        dict['paycost'] = request.session['cost']

        theatre = Theatres.objects.all().filter(id=request.session['theatre_id'])
        dict['theatreinfo'] = theatre[0]
        dict['theatreid']=request.session['theatre_id']
        dict['timevalue']=timevalue

        dict['bookedseats'] = bookedseats
        dict['request']=request
        request.session['payment']=True
        sendmailView(request)
        return render(request,'BookedInfo.html',context=dict)


def PaytmView(request,pk1,pk,t,selectedseats):
    dict={}
    dict['paycost'] = pk
    return render(request, 'BookedInfo.html', context=dict)

def MyWalletView(request,pk1,pk,t,selectedseats):
    dict={}
    dict['paycost'] = pk
    return render(request, 'BookedInfo.html', context=dict)

from django.core.mail import send_mail


def sendmailView(request):

    theatre = Theatres.objects.get(id=request.session['theatre_id'])


    subject = 'bookmymovie'
    from_email = ''

    to_email = [request.user.email]
    message='<div align="center"><div align="center" style="background-color:darkslateblue;width:40%;height:350px"><div align="center" >' \
            '<strong>Booked Information</strong><hr>'\
            '<strong>'+"MovieName: "+ theatre.Movie.MovieName+'</strong><br><br>'\
            '<strong>'+"TheatreName: "+theatre.TheatreName+'</strong><br><br>'\
            '<strong>'+"TheatreAddress: "+theatre.TheatreAddress+'</strong><br><br>'\
            '<strong>'+"SeatNumbers: "+request.session['bookedseats']+'</strong><br><br>'\
            '<strong>'+"Date of Movie: " + request.session['datevalue']+'</strong><br><br>'\
            '<strong>' + "MovieTime: " +request.session['timevalue']+ '</strong><br><br>'\
            '<br><strong>'+"Amount Paid:"+request.session['cost']+'/-</strong></div></div></div>'

    send_mail(subject="BookMyMovieTickets",message="",from_email=from_email,recipient_list=to_email,html_message=message)

