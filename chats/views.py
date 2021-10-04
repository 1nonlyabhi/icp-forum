from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from django.views import View
from django.contrib import messages
from django.db.models.query_utils import Q

from chats.forms import MessageForm, ThreadForm
from chats.models import MessageModel, ThreadModel
from notifications.models import Notification

# Create your views here.

# Chat Functionality

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        thread = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': thread
        }
        return render(request, 'chats/inbox.html', context)


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }
        return render(request, 'chats/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')

        if username == request.user.username:
            return HttpResponse("You can't message to yourself.")

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)
            
            if form.is_valid():
                thread = ThreadModel(user=request.user, receiver=receiver)
                thread.save()

                return redirect('thread', pk=thread.pk)

        except:
            messages.success(request, 'Try the correct username...')
            return redirect('create-thread')


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'chats/thread.html', context)


class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()

        notification = Notification.objects.create(
            notification_type=4,
            from_user=request.user,
            to_user=receiver,
            thread=thread
        )

        return redirect('thread', pk=pk)