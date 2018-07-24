from BookMyMovie.models import *
from django.contrib.auth.models import Permission,User
from django import forms



class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','email','first_name','last_name')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),

            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'})
        }

class UserInfoForm(forms.ModelForm):
    class Meta:
        model=UserInfo
        exclude=['User']
        widgets={

            'Wallet':forms.NumberInput(attrs={'class':'form-control'})
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model=Locations
        exclude=['id']
        widgets ={
            'LocationName':forms.TextInput(attrs={'class':'form-control'}),

        }

class MovieForm(forms.ModelForm):
    class Meta:
        model=Movies
        exclude=['id','Location']
        widgets={
            'MovieName':forms.TextInput(attrs={'class':'form-control'}),

            'MovieRating':forms.TextInput(attrs={'class':'form-control'}),
            'Language':forms.TextInput(attrs={'class':'form-control'}),
            'Genre':forms.TextInput(attrs={'class':'form-control'}),
            'trailer':forms.TextInput(attrs={'class':'form-control'})
        }
class TheatreForm(forms.ModelForm):
    class Meta:
        model=Theatres
        exclude=['id','Location','Movie']
        widgets={
            'TheatreName':forms.TextInput(attrs={'class':'form-control'}),
            'TheatreAddress':forms.TextInput(attrs={'class':'form-control'}),
            'TheatreRating':forms.NumberInput(attrs={'class':'form-control'})
        }