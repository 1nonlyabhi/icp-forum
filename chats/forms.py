from django import forms
from chats.models import MessageModel


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)


class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000)

    class Meta:
        model = MessageModel
        fields = ['body']