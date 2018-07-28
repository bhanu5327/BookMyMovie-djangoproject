from django import forms
class SignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name '})
    )

    last_name = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name '})
    )

    username = forms.CharField(
        max_length = 15,
        required=True,
        widget =forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'})
    )

    email = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'})
    )

    password = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password '})
    )
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length = 15,
        required=True,
        widget =forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'})
    )

    password = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password '})
    )
class ForgotPasswordForm(forms.Form):
    code = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '4-digit code'})
    )
# class SignUp(forms.Form):
#     # widgets = {
#     #     'FirstName': forms.TextInput(attrs={'class': 'form-control'}),
#     #     'LastName': forms.TextInput(attrs={'class': 'form-control'}),
#     #     'UserName': forms.TextInput(attrs={'class': 'form-control'}),
#     #     #'Password': forms.PasswordInput(attrs={'class': 'form-control'})
#     # }
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=100)
#     username = forms.CharField(max_length=100)
#     password= forms.CharField(widget=forms.PasswordInput)
#     email=forms.EmailField()

# class Login(forms.Form):
#     username = forms.CharField(max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput)