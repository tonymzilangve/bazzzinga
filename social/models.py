
from friend.models import Amigos
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

GENDER = [
    ['male', "Мужской"],
    ['female', "Женский"]
]

RELATIONSHIP = [
    ['complicated', "Все сложно"],
    ['single', "Словно Птица в Небесах"],
    ['meetsmb', "Есть с кем сходить в кино"],
    ['married', "Попал(а) в оковы"],
    ['soloway', "Живу с кошкой/собакой"],
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Юзер")
    fio = models.CharField(max_length=30,  blank=True, null=True, verbose_name="Как звать по паспорту?")
    amigos = models.ForeignKey(Amigos, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Друзья", related_name='amigos')
    nick = models.CharField(max_length=30, blank=True, null=True, verbose_name="Nomad")

    avatar = models.FileField(verbose_name="АвадаКедавра", null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="Мой путь")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name="De donde eres, pendejo?")

    visited = models.CharField(max_length=50, blank=True, null=True, verbose_name="3 последние посещенные страны")
    planning = models.CharField(max_length=50, blank=True, null=True, verbose_name="Куда хочешь поехать?")
    language = models.CharField(max_length=50, blank=True, null=True, verbose_name="Якою мовою розмовляэш?")

    birthday = models.DateField(null=True, blank=True, verbose_name="День народження")
    gender = models.CharField(max_length=10, null=True, verbose_name="Пол", choices=GENDER, default="male")
    relationship = models.CharField(max_length=20, verbose_name="Статус отношений", choices=RELATIONSHIP, default="none")

    mobile = models.CharField(max_length=20, blank=True, null=True, verbose_name="На созвоне")

    def __str__(self):
        return self.nick

    def get_absolute_url(self):
        return reverse('profile', kwargs={'nick': self.nick})

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['id']


class Post(models.Model):
    datetime = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="posts")
    text = models.CharField(max_length=1000, verbose_name="Текст", null=True, blank=True)
    image = models.FileField(verbose_name="Картинка", null=True, blank=True)

    class Meta:
        ordering = ["-datetime"]


class Comment(models.Model):
    datetime = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост", related_name="comments")
    text = models.CharField(max_length=1000, verbose_name="Текст", null=True, blank=True)

    class Meta:
        ordering = ["datetime"]
