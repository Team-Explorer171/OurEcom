from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from App_login.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

