from .models import Post, Profile
from django import forms

""" КАКИЕ ЕСТЬ:
* LoginForm  * RegisterForm  * ProfileForm    * PostForm """


class LoginForm(forms.Form):
    username = forms.CharField(label="Ник")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="Позывной")
    email = forms.EmailField(label="Email", required=False)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)

    def is_valid(self):
        """ Проверка Заполнения Формы """
        valid = super(RegisterForm, self).is_valid()
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            self.add_error("password_confirm", "Пароли не совпадают")
            return False
        return valid


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'amigos']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
