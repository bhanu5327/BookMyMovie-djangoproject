from django.urls import path
from BookMyMovie import views
from .views.Movies import *
from .views.Theatres import *
from .views.seats import *
from .views.Payment import *
from .views.UserProfile import *
app_name='BookMyMovieApp'
urlpatterns=[

    path('userdetails/<str:pk>/',UserDetailsView.as_view(),name='userdetails'),
    path('userdetails/<str:pk>/edit/',EditUserDetailsView.as_view(),name='edituserdetails'),


    path('signup/',SignUpView.as_view(),name="signup_html"),
    path('login/',LoginView.as_view(),name="login_html"),
    path('logout/',LogoutView,name="logout_html"),
    path('resetpassword/step1/',ForgotPassword1View.as_view(),name="forgotpassword1_html"),
    path('resetpassword/step2/',ForgotPassword2View.as_view(),name="forgotpassword2_html"),
    path('resetpassword/step3/',ForgotPassword3View.as_view(),name="forgotpassword3_html"),

    path('locations/',LocationsListView.as_view(),name='ViewLocations'),
    path('locations/add/',CreateLocationView.as_view(),name='AddLocation'),
    path('locations/<str:pk>/edit/',EditLocationView.as_view(),name='EditLocation'),
    path('locations/<str:pk>/delete/',DeleteLocationView.as_view(),name='DeleteLocation'),

    path('search/',getsearchresult,name="searchmovie"),

    path('locations/<str:pk>/movies/',MoviesListView.as_view(),name='ViewMovies'),
    path('locations/<str:pk1>/movies/<str:pk>/',DetailedMovieView.as_view(),name='ViewMovie'),
    path('locations/<str:pk>/movies/add/movie/',CreateMovieView.as_view(),name='AddMovie'),
    path('locations/<str:pk1>/movies/<str:pk>/edit/',EditMovieView.as_view(),name='EditMovie'),
    path('locations/<str:pk1>/movies/<str:pk>/delete/',DeleteMovieView.as_view(),name='DeleteMovie'),

    path('locations/<str:pk1>/movies/<str:pk>/Theatres/',TheatresListView.as_view(),name='ViewTheatres'),
    path('locations/<str:pk1>/movies/<str:pk>/Theatres/add/',CreateTheatreView.as_view(),name='AddTheatre'),
    path('locations/<str:pk2>/movies/<str:pk1>/Theatres/<str:pk>/edit/',EditTheatreView.as_view(),name='EditTheatre'),
    path('locations/<str:pk2>/movies/<str:pk1>/Theatres/<str:pk>/delete/',DeleteTheatreView.as_view(),name='DeleteTheatre'),

    path('Theatres/<str:pk>/<str:datevalue>/<str:timevalue>/seats/',SeatsListView.as_view(),name='ViewSeats'),
    path('Theatres/<str:pk1>/seats/<str:datevalue>/<str:timevalue>/<str:bookedseats>/cost/<str:pk>/<str:log>/',LoginNeeded,name='LoginNeeded'),
    path('seats/',JustLogged,name='JustLogged'),
    path('Theatres/<str:pk1>/seats/<str:datevalue>/<str:timevalue>/<str:bookedseats>/cost/<str:pk>/',BookingSummaryView,name='BookingSummary'),
    path('paymentoptions/creditcard/',CreditcardView,name='Creditcard'),
    path('paymentoptions/paytm/',CreditcardView,name='Paytm'),
    path('paymentoptions/mywallet/',CreditcardView,name='MyWallet'),
    path('sharetomail/<str:pk>/',sendmailView,name='sendmail'),

    #path('api/signup/', SignupView.as_view(), name=signupview)
    #path('/api/login/',LoginView.as_view(),name=loginview)

    # path('api/locations/',LocationsListView.as_view()),
    # path('api/locations/<str:pk>/',LocationsDetailedView.as_view()),
    # path('api/locations/<str:pk>/movies/',MoviesListView.as_view()),
    # path('api/locations/<str:pk1>/movies/<str:pk>/', MoviesDetailedView.as_view()),
    # path('api/locations/<str:pk1>/movies/<str:pk>/theatres/', TheatresListView.as_view()),
    # path('api/locations/<str:pk2>/movies/<str:pk1>/theatres/<str:pk>/', TheatresDetailedView.as_view()),
    #path('api/location/<str:pk>/')

]