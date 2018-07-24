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
    index = 0
    theatre = Theatres.objects.get(id=request.session['theatre_id'])
    while (bookedseats[index:index + 2] != ''):
        seat = SeatsInfo(SeatNumber=bookedseats[index:index + 2], SeatCost=100,
                         MovieDate=datevalue,
                         MovieTime=timevalue, BookedDateTime=str(datetime.datetime.now(tz=timezone.utc)))
        seat.Theatre = theatre
        seat.User = request.user
        seat.save()
        index = index + 2
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
    s=""
    for i in bookedseats:
        if i in string.ascii_uppercase and s!='':
            s=s+','+i
        else:
            s=s+i


    dict['datevalue']=datevalue
    dict['bookedseats']=s
    request.session['bookedseats']=s
    request.session['cost']=pk
    request.session['payment'] = False
    return render(request, 'BookingSummary.html', context=dict)

from django.template.loader import render_to_string, get_template
from django.core.mail.message import EmailMultiAlternatives

def CreditcardView(request):
    dict={}
    dict['paycost'] = request.session['cost']

    theatre = Theatres.objects.all().filter(id=request.session['theatre_id'])
    dict['theatreinfo'] = theatre[0]
    dict['theatreid']=request.session['theatre_id']
    dict['timevalue']=request.session['timevalue']
    s = ""
    for i in request.session['bookedseats']:
        if i in string.ascii_uppercase and s != '':
            s = s + ',' + i
        else:
            s = s + i
    dict['bookedseats'] = request.session['bookedseats']
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
    message='<div align="center" >' \
            '<div align="center"><strong>Booked Information</strong></div><hr>'
    message+=' <img src="'+str(theatre.Movie.MoviePoster.url)+'" width="130px" height="180px" align="left"/>'
    message+='<strong>'+"MovieName: "+ theatre.Movie.MovieName+'</strong><br><br>'
    message+='<strong>'+"TheatreName: "+theatre.TheatreName+'</strong><br><br>'
    message+='<strong>'+"TheatreAddress: "+theatre.TheatreAddress+'</strong><br><br>'
    message+='<div align="center"><strong>'+"SeatNumbers: "+request.session['bookedseats']+'</strong></div><br><br>'
    message += '<div align="center"><strong>' + "Date of Movie: " + request.session['datevalue'] + '</strong></div><br><br>'
    message += '<div align="center"><strong>' + "MovieTime: " +request.session['timevalue']+ '</strong></div><br><br>'
    message+='<br><div align="center"><strong>'+"Amount Paid:"+request.session['cost']+'/-</strong></div></div><br>'

    send_mail(subject="BookMyMovieTickets",message="",from_email=from_email,recipient_list=to_email,html_message=message)

