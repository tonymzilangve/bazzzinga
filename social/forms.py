from django.contrib.auth.models import User
from .models import Post, Profile
from django import forms

""" * LoginForm  * RegisterForm  * ProfileForm  * PostForm """


class LoginForm(forms.Form):
    username = forms.CharField(label="Ник")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="Позывной")
    email = forms.EmailField(label="Email", required=False)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)

    def no_dublicate(self):
        """ Проверка Заполнения Формы """
        valid = super(RegisterForm, self).is_valid()

        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['password_confirm']

        if pass1 != pass2:
            self.add_error("password_confirm", "Пароли не совпадают")
            return False
        elif User.objects.filter(username=username).exists() or Profile.objects.filter(nick=username).exists():
            self.add_error("username", "Данный username занят!")
            return False
        elif User.objects.filter(email=email).exists():
            self.add_error("email", "Пользователь с таким email уже зарегистрирован!")
            return False
        return valid


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'amigos']

    def nick_is_free(self):
        if User.objects.filter(username=self.nick).exists() or Profile.objects.filter(nick=self.nick).exists():
            self.add_error("nick", "Данный nick занят!")
            return False
        return True


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
