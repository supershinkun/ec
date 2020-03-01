from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *
from django.core.exceptions import ValidationError

class LoginForm(AuthenticationForm):
    """ログインフォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'zipcode', 'address1', 'address2', 'address3')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.label == '郵便番号':
                field.widget.attrs['placeholder'] = field.label + ' (8890014)'
                continue
            field.widget.attrs['placeholder'] = field.label

    # 本登録に失敗してactivateされてないアドレスを再登録できるようにDBから削除
    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'zipcode', 'address1', 'address2', 'address3')