from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import logout
from django.contrib import messages
from friend.models import Amigos, FriendRequest

from .models import Profile, Post, Comment
from .forms import ProfileForm, PostForm, RegisterForm, LoginForm


class RegisterView(TemplateView):
    """ РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ """
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()

        if request.method == 'POST':
            form = RegisterForm(request.POST)

            if form.is_valid() and form.no_dublicate():
                username = request.POST.get('username', None)
                email = request.POST.get('email', None)
                password = request.POST.get('password', None)

                User.objects.create_user(username, email, password)
                user = authenticate(request, username=username, email=email, password=password)
                login(request, user)

                form1 = ProfileForm(instance=self.get_profile(request.user))
                prof = form1.save(commit=False)
                prof.user = request.user
                prof.nick = username
                prof.email = email
                prof.save()

                amigos = Amigos.objects.create(user=request.user)
                messages.success(request, "Добро пожаловать в семью!\nДополните информацию в Ваш профиль!")

                return redirect(reverse("edit_profile"))

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None


class LaUne(TemplateView):
    timeline_template_name = "timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
           return redirect(reverse("login"))

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(reverse("home"))
        a = Amigos.objects.filter(user=request.user)
        amigos = a[0].friends.all()
        context = {
            'posts': Post.objects.all(),
            'requests': FriendRequest.objects.filter(receiver=request.user),
            'amigos': amigos
        }
        return render(request, self.timeline_template_name, context)


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            context = {
                'form': form
            }

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse("home"))
                else:
                    context['error'] = "Я стер твой файл. Теперь ты никто. Придется начинать все сначала("
                    return render(request, self.template_name, context)
            else:
                context['error'] = "Данной комбинации Логин/Пароль НЕ существует в системе\nЗарегистрируйтесь!"
                return render(request, self.template_name, context)

        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


def ProfilePage(request, nick):
    selected_user = Profile.objects.get(nick=nick)
    user = request.user

    if user.profile != selected_user:
        info = selected_user
        try:
            request1 = FriendRequest.objects.get(sender=selected_user.user, receiver=user, is_active=True)
        except:
            request1 = None

        try:
            request2 = FriendRequest.objects.get(sender=user, receiver=selected_user.user, is_active=True)
        except:
            request2 = None

        friend = Amigos.objects.get_or_create(user=selected_user.user)
        friends = friend[0].friends.all()

    else:
        info = request.user.profile
        request1 = None
        request2 = None
        friends = None

    q = Amigos.objects.get_or_create(user=user)
    ami = q[0].friends.all()

    context = {  # все понял!
        'selected_user': info,  # self.request.user.profile ; передаем ТЕКУЩЕГО юзера
        'sel_user_friends': friends,
        'request1': request1,   # встречный запрос (МНЕ!)
        'request2': request2,  # иcходящий
        'amigos': ami
    }

    return render(request, "registration/profile.html", context)


class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        """указываем Форме ссылку на профиль, чтобы она НЕ создавала новый обьект, а изменяла существующий"""
        form = ProfileForm(instance=self.get_profile(request.user))
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                messages.success(request, "Профиль успешно обновлен!")
                return redirect(reverse("home"))
        return render(request, self.template_name, {'form': form})

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None


class PostCommentView(View):
    def dispatch(self, request, *args, **kwargs):
        post_id = request.GET.get("post_id")
        comment = request.GET.get("comment")

        if comment and post_id:
            post = Post.objects.get(pk=post_id)
            comment = Comment(text=comment, post=post, author=request.user)
            comment.save()
            return render(request, "blocks/comment.html", {'comment': comment})
        return HttpResponse(status=500, content="")


class SearchView(TemplateView):   # works
    template_name = 'search.html'

    def dispatch(self, request, *args, **kwargs):
        context = {}
        user = request.user
        if request.method == 'GET':
            query = request.GET.get("q")
            if len(query) > 0:
                search = Profile.objects.filter(Q(nick__icontains=query) | Q(fio__icontains=query)).distinct()
            profiles = []

            for profile in search:
                if profile != request.user.profile:
                    profiles.append((profile, False))

                    try:  # [WorkAet]
                        request1 = FriendRequest.objects.get(sender=profile.user, receiver=user,
                                                             is_active=True)
                    except:
                        request1 = None

                    try:  # [WORKает]
                        request2 = FriendRequest.objects.get(sender=user, receiver=profile.user,
                                                             is_active=True)
                    except:
                        request2 = None

            ami = Amigos.objects.filter(user=user)
            amigos = ami[0].friends.all()

            context['profiles'] = profiles
            context['amigos'] = amigos
            context['request1'] = request1
            context['request2'] = request2

        return render(request, self.template_name, context)



