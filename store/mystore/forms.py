from django import forms

class LoginForm(forms.Form):
    user_name = forms.IntegerField(label='UserName')
    password = forms.PasswordInput()