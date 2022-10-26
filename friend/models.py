from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone


""" ADD / REMOVE / UNFRIEND / IS_MUTUAL """
class Amigos(models.Model):    # Friend_List
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")   #OnetoOne?
    # settings.AUTH_USER_MODEL

    def __str__(self):
        return self.user.profile.nick + "'s friends"

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            # self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        remover_amigos = self
        remover_amigos.remove_friend(removee)
        amigos = Amigos.objects.get(user=removee)
        amigos.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False

    """ Admin panel """
    class Meta:
        verbose_name = 'FriendList'
        verbose_name_plural = 'FriendLists'


class FriendRequest(models.Model):
    """ ACCEPT / DECLINE / CANCEL """

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Request from " + self.sender.username + " to " + self.receiver.username

    def accept(self):
        receiver_amigos = Amigos.objects.get(user=self.receiver)   # get_or_create?
        if receiver_amigos:
            receiver_amigos.add_friend(self.sender)   # Принимаем с той стороны
            sender_amigos = Amigos.objects.get(user=self.sender)
            if sender_amigos:
                sender_amigos.add_friend(self.receiver)   # принимаем с этой стороны
                self.is_active = False
                self.delete()

    """ Request sent to you - you decline """
    def decline(self):
        self.is_active = False
        self.delete()

    """ You sent a request to smb - you cancel it """
    def cancel(self):
        self.is_active = False
        self.delete()

    """ Admin Panel """
    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'
        ordering = ['-timestamp']


