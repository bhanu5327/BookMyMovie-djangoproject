from django.views.generic import ListView, CreateView, UpdateView, DeleteView,View,DetailView

from BookMyMovie.forms import LocationForm, MovieForm
from BookMyMovie.models import *
from django.shortcuts import *
from django.urls import *


from .auth import *
from django.contrib.auth.models import Permission,User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth import logout
import random
raise_exception=True
Location_Global=1

class SignUpView(View):
    def get(self,request):
        form_class = SignUpForm

        return render(request,template_name='Register.html',context={'form':form_class})
    def post(self,request,*args,**kwargs):
        signup_form=SignUpForm(request.POST)
        if signup_form.is_valid():
            user=User.objects.create_user(**signup_form.cleaned_data)
            UserInfo.objects.create(User=user,Photo='images/person.jpg',Wallet=0)

            # user.first_name=cleandata['FirstName']
            # user.last_name=cleandata['LastName']
            # user.password=cleandata['Password']
            # user.username=cleandata['UserName']
        return redirect('BookMyMovieApp:login_html')
class LoginView(View):
    def get(self,request):
        try:
            if (request.session['step3'] == False):
                request.session['step3f'] = False
        except:
            pass
        request.session['step1f']=False
        request.session['step2f'] = False
        request.session['step3'] = False
        request.session['step2'] = False
        request.session['step1'] = False
        form_class = LoginForm
        return render(request,template_name='Login.html',context={'form':form_class})

    def post(self,request,*args,**kwargs):

        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            try:
                if request.session['timevalue']:
                    return redirect('BookMyMovieApp:JustLogged')
            except:
                pass
            return redirect('BookMyMovieApp:ViewLocations')
        else:
            return redirect('BookMyMovieApp:login_html')

def LogoutView(request):
    logout(request)
    return redirect('BookMyMovieApp:login_html')

class ForgotPassword1View(View):
    def get(self, request):
        if request.session['step1']==False:
            request.session['step1f'] = False
        request.session['step1'] = False
        form_class=LoginForm
        return render(request,'ForgotPassword1.html',context={'form':form_class})
    def post(self,request,*args,**kwargs):
        request.session['step1']=request.POST['username']
        try:
            user=User.objects.get(username=request.POST['username'])
            return redirect('BookMyMovieApp:forgotpassword2_html')
        except:
            request.session['step1f']=True
            return redirect('BookMyMovieApp:forgotpassword1_html')


class ForgotPassword2View(View):
    def get(self, request):
        if request.session['step1']:
            if request.session['step2']==False:
                request.session['step2f'] = False
            request.session['step2'] = False
            request.session['step1f']=False
            form_class=ForgotPasswordForm
            code = random.randint(1000, 9999)
            user = User.objects.get(username=request.session['step1'])
            uname=user.username
            email=user.email
            request.session['step2']=str(code)
            sendmailView(request, code, uname, email)
            return render(request,'ForgotPassword2.html',context={'form':form_class,'user':user})
        else:
            return render(request,'NOTFOUND.html',context={})
    def post(self,request,*args,**kwargs):


        if(request.session['step2']==request.POST['code']):
            request.session['step2'] = request.POST['code']
            return redirect('BookMyMovieApp:forgotpassword3_html')
        else:
            request.session['step2'] = request.POST['code']
            request.session['step2f'] = True
            return redirect('BookMyMovieApp:forgotpassword2_html')
class ForgotPassword3View(View):
    def get(self, request):
        if request.session['step2'] and request.session['step1']:
            request.session['step2f'] = False
            form_class = LoginForm
            return render(request, 'ForgotPassword3.html', context={'form': form_class})
        else:
            return render(request,'NOTFOUND.html',context={})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.session['step1'])
        request.session['step3']=request.POST['password']
        user.set_password(request.POST['password'])
        user.save()
        return redirect('BookMyMovieApp:login_html')

from django.core.mail import send_mail
def sendmailView(request,code,uname,email):

    subject = 'bookmymovie'
    from_email = ''
    message='<div align="center"><div align="center">'\
            '<strong>UserName:'+str(uname)+'</strong><br>'\
            '<strong>Verification-Code:'+str(code)+'</strong></div></div>'
    to_email = [email]


    send_mail(subject="BookMyMovieTickets",message="",from_email=from_email,recipient_list=to_email,html_message=message)
class LocationsListView(ListView):

    model = Locations
    context_object_name = 'Locations_List'

    template_name = 'LocationForm.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(LocationsListView,self).get_context_data(**kwargs)
        self.request.session['location_id']=False
        self.request.session['movie_id'] = False
        self.request.session['theatre_id'] = False
        self.request.session['bookedseats']=False
        self.request.session['timevalue']=False
        self.request.session['datevalue']=False
        self.request.session['movieinfo']=False
        self.request.session['payment']=False
        return context
class CreateLocationView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = 'BookMyMovieApp.add_Locations'
    permission_denied_message = 'k8ijuhg'
    raise_exception = True
    login_url = '/login/'

    model=Locations
    form_class = LocationForm
    template_name = 'form.html'
    success_url = reverse_lazy('BookMyMovieApp:ViewLocations')
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(CreateLocationView,self).get_context_data(**kwargs)
        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context

class EditLocationView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    permission_required = 'BookMyMovieApp.change_Locations'
    permission_denied_message = 'k8ijuhg'
    raise_exception = True
    model = Locations
    form_class = LocationForm
    template_name = 'form.html'
    success_url = reverse_lazy('BookMyMovieApp:ViewLocations')
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(EditLocationView,self).get_context_data(**kwargs)
        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context

class DeleteLocationView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/login/'
    permission_required = 'BookMyMovieApp.delete_Locations'
    permission_denied_message = 'k8ijuhg'
    raise_exception = True
    model = Locations
    form_class = LocationForm
    template_name = 'DeleteForm.html'
    success_url = reverse_lazy('BookMyMovieApp:ViewLocations')
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(DeleteLocationView,self).get_context_data(**kwargs)
        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context

def getsearchresult(request):

    MoviesList=Movies.objects.all().filter(Location_id=Location_Global)
    query=request.GET['suggestion']

    if query:

        l = []
        for i in MoviesList:
            if ((i.MovieName).lower()).__contains__(query.lower()):
                l.append(i)
    else:
        l = []

    return render(request,'searchresult.html',{'searchresult':l,'location_id':Location_Global})

class MoviesListView(ListView):

    model = Movies
    # context_object_name = 'Movies_List'
    template_name = 'MovieForm.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        global Location_Global
        Location_Global=self.kwargs['pk']
        self.request.session['location_id']=self.kwargs['pk']
        self.request.session['movie_id'] = False
        self.request.session['theatre_id'] = False
        self.request.session['bookedseats'] = False
        self.request.session['timevalue'] = False
        self.request.session['datevalue'] = False
        self.request.session['movieinfo'] = False
        self.request.session['payment'] = False


        context=super(MoviesListView,self).get_context_data(**kwargs)
        context['location_id'] = self.kwargs['pk']
        MoviesCarouselList=Movies.objects.all().filter(Location_id=self.kwargs['pk']).order_by('-id')
        context['MoviesCarouselList'] = MoviesCarouselList
        if len(MoviesCarouselList)>0:
            context['Movie1'] = MoviesCarouselList[0]
        if len(MoviesCarouselList) > 1:
            context['Movie2'] = MoviesCarouselList[1]
            if len(MoviesCarouselList) > 2:
                context['Movie3'] = MoviesCarouselList[2]


        MoviesList=Movies.objects.all().filter(Location_id=self.kwargs['pk'])

        query=self.request.GET.get("suggestion")

        l=MoviesList
        if query:

            l=[]
            for i in MoviesList:
                if ((i.MovieName).lower()).__contains__(query.lower()):
                    l.append(i)
        else:
            l=MoviesList

        p = []
        p1 = []
        MoviesList=l
        for i in range(len(MoviesList)):
            if i % 3 == 0 and i != 0:
                p.append(p1)
                p1 = []
            p1.append(MoviesList[i])
        p.append(p1)
        MoviesList = p
        context['Movies_List']=MoviesList
        Languages_List = set()
        Genres_List = set()
        temp = Movies.objects.all()
        for i in temp:
            Languages_List.add(i.Language)
            Genres_List.add(i.Genre)
        context['Languages_List'] = Languages_List
        context['Genres_List'] = Genres_List


        context['s'] = ""
        context['g'] = ""

        return context
    def post(self,request,*args,**kwargs):

        str=request.POST['selectedLanguages']
        selectedLanguages=str.split()
        str = request.POST['selectedGenres']
        selectedGenres = str.split()
        MoviesList=Movies.objects.all().filter(Location_id=self.kwargs['pk'])
        z=[]
        if selectedLanguages!=[] and selectedGenres!=[]:
            for i in MoviesList:
                if i.Language in selectedLanguages and i.Genre in selectedGenres:
                    z.append(i)
            MoviesList = z
        elif selectedLanguages!=[]:
            for i in MoviesList:
                if i.Language in selectedLanguages:
                    z.append(i)
            MoviesList = z
        elif selectedGenres!=[]:
            for i in MoviesList:
                if i.Genre in selectedGenres:
                    z.append(i)
            MoviesList = z
        p = []
        p1 = []

        for i in range(len(MoviesList)):
            if i % 4 == 0 and i != 0:
                p.append(p1)
                p1 = []
            p1.append(MoviesList[i])
        p.append(p1)
        MoviesList = p
        dict={}
        dict['Movies_List']=MoviesList
        dict['location_id'] = self.kwargs['pk']
        MoviesCarouselList = Movies.objects.all().filter(Location_id=self.kwargs['pk']).order_by('-id')
        MoviesCarouselList = MoviesCarouselList[:3]
        dict['MoviesCarouselList'] = MoviesCarouselList
        dict['Movie1'] = MoviesCarouselList[0]
        if len(MoviesCarouselList)>0:
            dict['Movie2'] = MoviesCarouselList[1]
            if len(MoviesCarouselList)<1:
                dict['Movie3'] = MoviesCarouselList[2]
        Languages_List = set()
        Genres_List = set()
        temp = Movies.objects.all()
        for i in temp:
            Languages_List.add(i.Language)
            Genres_List.add(i.Genre)
        dict['Languages_List'] = Languages_List
        dict['Genres_List'] = Genres_List
        dict['selectedLanguages']=selectedLanguages
        dict['selectedGenres']=selectedGenres

        dict['s']=" ".join(selectedLanguages)
        dict['g']=" ".join(selectedGenres)

        return render(request,"MovieForm.html",dict)




class DetailedMovieView(DetailView):

    model = Movies
    template_name = 'MovieInfo.html'
    def get_context_data(self, *, object_list=None, **kwargs):

        Movie=Movies.objects.get(id=self.kwargs['pk'])
        dict={}
        dict['location_id']=self.kwargs['pk1']
        self.request.session['location_id']=self.kwargs['pk1']
        self.request.session['movie_id'] = self.kwargs['pk']
        self.request.session['movieinfo']=True
        self.request.session['theatre_id'] = False
        self.request.session['bookedseats'] = False
        self.request.session['timevalue'] = False
        self.request.session['datevalue'] = False
        self.request.session['payment'] = False
        dict['movie']=Movie
        return dict



class CreateMovieView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = '/login/'
    permission_required = 'BookMyMovieApp.add_Movies'
    permission_denied_message = 'k8ijuhg'
    raise_exception = True
    model=Movies
    form_class = MovieForm
    template_name = 'form.html'
    def post(self, request, *args, **kwargs):
        location=Locations.objects.get(id=self.kwargs['pk'])
        movie_form=MovieForm(request.POST,request.FILES)

        if movie_form.is_valid():
            movie=movie_form.save(commit=False)

            movie.Location=location
            movie.save()

        return redirect('BookMyMovieApp:ViewMovies', pk=self.kwargs['pk'])

class EditMovieView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    permission_required = 'BookMyMovieApp.change_Movies'
    permission_denied_message = 'k8ijuhg'
    raise_exception = True
    model = Movies
    form_class = MovieForm
    template_name = 'form.html'

    def post(self, request, *args, **kwargs):

        movie=Movies.objects.get(id=self.kwargs['pk'])
        movie_form=MovieForm(request.POST,request.FILES,instance=movie)
        if movie_form.is_valid():
            movie=movie_form.save(commit=True)

        return redirect('BookMyMovieApp:ViewMovies', pk=self.kwargs['pk1'])


class DeleteMovieView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/login/'
    permission_required = 'BookMyMovieApp.delete_Movies'
    permission_denied_message = 'k8ijuhg'
    raise_exception = True
    model = Movies
    template_name = 'deleteform.html'
    def post(self,request,*args,**kwargs):
        movie=Movies.objects.get(id=self.kwargs['pk'])
        movie.delete()


        return redirect('BookMyMovieApp:ViewMovies',pk=self.kwargs['pk1'])
