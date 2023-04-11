from django import forms
from django.contrib.auth.forms import UserCreationForm ,UsernameField
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm  , AuthenticationForm

class SignUpForm(UserCreationForm):

    
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'class': 'form-control bg-transparent mb-3' , 'placeholder': 'Username'}))
    

    password1 = forms.CharField(
        
        label=False,
        strip=False,
        widget=forms.PasswordInput(attrs={'class' : 'form-control bg-transparent mb-3' , 'placeholder': 'Password'}),
        # help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'class' : 'form-control bg-transparent mb-3', 'placeholder': 'Confirm Password'}),
        strip=False,
        # help_text=_("Enter the same password as before, for verification."),
    )


    email = forms.EmailField(
        label=False,
        widget=forms.EmailInput(attrs={'class' : 'form-control bg-transparent mb-3', 'placeholder': 'Email'})
                            )


    class Meta:
        model = User
        fields = ("username","email")
    


class SignInForm(AuthenticationForm):
    username = UsernameField(
    label=False,    
    widget=forms.TextInput(attrs={'autofocus': True , 'class': 'form-control bg-transparent mb-3' , 'placeholder': 'Username'}))


    password = forms.CharField(
    label=False,    
    strip=False,widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control bg-transparent mb-3' ,  'placeholder': 'Password'}),
    )