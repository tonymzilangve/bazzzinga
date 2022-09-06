from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from social.models import Profile
from .models import FriendRequest, Amigos
from django.contrib import messages


def friends(request, nick, *args, **kwargs):
    context = {}
    user = request.user
    context['amigos'] = Amigos.objects.filter(user=user)

    friend_requests = FriendRequest.objects.filter(receiver=user)
    context['request_list'] = friend_requests

    if user.is_authenticated:
        try:
            this_user = Profile.objects.get(nick=nick)   #this_user
            context['this_user'] = this_user
        except Profile.DoesNotExist:
            context['error'] = 'That user does not exist.'
            return render(request, "friend_list.html", context)

        try:
            friend_list = Amigos.objects.get_or_create(user=this_user.user)
        except Amigos.DoesNotExist:
            context['error'] = f'Could not find a friends list for {this_user.nick}'
            return render(request, "friend_list.html", context)

        """ not your profile """
        if user.profile != this_user:
            if not user in friend_list[0].friends.all():  # you're not friends
                context['error'] = 'You must be friends to view their friends list.'
                return render(request, "friend_list.html", context)

        amigoss = True
        friends = []  # [(account1, True), (account2, False), ...]
        auth_user_friend_list = Amigos.objects.get_or_create(user=user)
        for friend in friend_list[0].friends.all():
            if friend != request.user:
                friends.append((friend, auth_user_friend_list[0].is_mutual_friend(friend)))

        context['friends'] = friends

        if friends is None:
            context['error'] = 'Ты - волк-одиночка!'
        else:
            context['amigos'] = friends
    else:
        context['error'] = 'Please, register!'

    try:  # [WorkAet]
        request1 = FriendRequest.objects.get(sender=this_user.user, receiver=user,
                                             is_active=True)  # добавить user.profile??
    except:
        request1 = None

    try:  # [WORKает]
        request2 = FriendRequest.objects.get(sender=user, receiver=this_user.user,
                                             is_active=True)  # + profile??/
    except:
        request2 = None

    context['amigoss'] = amigoss
    context['request1'] = request1
    context['request2'] = request2
    return render(request, "friend_list.html", context)


def friend_requests(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        # user_id = kwargs.get("user_id")
        # profile = Profile.objects.get(pk=user_id)
        # if profile == user:
        requests = FriendRequest.objects.filter(receiver=user, is_active=True)
        context['requests'] = requests
        # else:
        #     return HttpResponse("You can't view another users friend requests.")
    else:
        redirect("login")
    return render(request, "requests.html", context)   # было search


def send_friend_request(request, nick, *args, **kwargs):
    user = request.user
    context = {}
    context['requests'] = FriendRequest.objects.filter(receiver=user, is_active=True)

    receiver = Profile.objects.get(nick=nick)
    if receiver == user.profile:
        context['response'] = "Нельзя отправить запрос самому себе!"

    elif user.is_authenticated:
        receiver = Profile.objects.get(nick=nick)
        if receiver == user:
            context['response'] = "Нельзя отправить запрос самому себе!"
        try:
            requesta = FriendRequest.objects.get(sender=user, receiver=receiver.user)
        except:
            requesta = None

        if requesta:
            if requesta.is_active:
                context['response'] = "Вы уже отправляли запрос этому пользователю!"
                return render(request, "requests.html", context)

        friend_request = FriendRequest(sender=user, receiver=receiver.user)
        friend_request.save()
        context['response'] = "Запрос отправлен!"

        if context['response'] is None:
            # payload['response'] = "Что-то пошло не так..."
            messages.success(request, "Что-то пошло не так...")

    else:
        messages.success(request, "Сначала надо авторизироваться!")

    return render(request, "requests.html", context)


def accept_friend(request, *args, **kwargs):   # to Template
    template_name = "requests.html"
    user = request.user
    context = {}

    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.accept()
                    context['response'] = "Friend request accepted"
                else:
                    context['response'] = "Something went wrong"
            else:
                context['response'] = "That is not your request to accept."
        else:
            context['response'] = "Unable to accept that friend request."
    else:
        context['response'] = "You must be authenticated to accept a friend request."
    return render(request, template_name, context)


def decline_friend(request, nick, *args, **kwargs):
    template_name = "requests.html"
    user = request.user
    context = {}
    nofriend = Profile.objects.get(nick=nick)

    if request.method == "GET" and user.is_authenticated:
        try:
            friend_request = FriendRequest.objects.get(sender=request.user, receiver=nofriend.user)
        except:
            friend_request = None
        try:
            friend_reverse = FriendRequest.objects.get(sender=nofriend.user, receiver=request.user)
        except:
            friend_reverse = None

        if not friend_request is None:
            friend_request.decline()
            context['response'] = "Friend request declined!"
        elif not friend_reverse is None:
            friend_reverse.decline()
            context['response'] = "Friend request declined!"
        else:
            context['response'] = "Something went wrong"
    else:
        context['response'] = "You must be authenticated to decline a friend request."
    return render(request, template_name, context)


def cancel_request(request, *args, **kwargs):
    template_name = "requests.html"
    user = request.user
    context = {}

    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = Profile.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
            except Exception as e:
                context['response'] = "Nothing to cancel. Friend request doesn't exist."

            if len(friend_requests) > 1:
                for request in friend_requests:
                    request.cancel()
                context['response'] = "Friend request cancelled!"
            else:
                friend_requests.first().cancel()
                context['response'] = "Friend request cancelled!"
        else:
            context['response'] = "Unable to cancel request."
    else:
        context['response'] = "You must be authenticated to cancel a friend request."
    return render(request, template_name, context)


def remove_friend(request, nick, *args, **kwargs):
    template_name = "friend_list.html"
    user = request.user
    context = {}

    miamigos = Amigos.objects.get(user=user)
    context['amigos'] = miamigos
    friend_requests = FriendRequest.objects.filter(receiver=user)
    context['request_list'] = friend_requests

    if request.method == "GET" and user.is_authenticated:
        try:
            removee = Profile.objects.get(nick=nick)
            print(removee)

            amigos = Amigos.objects.get(user=removee.user)
            miamigos.unfriend(removee.user)
            context['response'] = "Successfully removed that friend"
        except Exception as e:
            context['response'] = f"Something went wrong: {str(e)}."
    else:
        context['response'] = "You must be authenticated to remove a friend request."

    return render(request, template_name, context)