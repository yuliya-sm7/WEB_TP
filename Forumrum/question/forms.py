from django import forms


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
