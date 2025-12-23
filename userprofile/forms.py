from django import forms
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='确认密码')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_confirm_password(self):
        data = self.cleaned_data
        if data.get('password') == data.get('confirm_password'):
            return data.get('confirm_password')
        raise forms.ValidationError("两次密码不一致,请重试。")
