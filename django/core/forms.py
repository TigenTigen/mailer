from django import forms
from django.contrib.auth import get_user_model
from core.models import Subscriber, Massage, MailingList

USER_MODEL = get_user_model()

class SubscriberForm(forms.ModelForm):
    mailinglist = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=MailingList.objects.all(), disabled=True)

    class Meta:
        model = Subscriber
        fields = ['mailinglist', 'email']

class MassageForm(forms.ModelForm):
    mailinglist = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=MailingList.objects.all(), disabled=True)

    class Meta:
        model = Massage
        fields = ['mailinglist', 'subject', 'body']

class MailingListForm(forms.ModelForm):
    owner = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=USER_MODEL.objects.all(), disabled=True)

    class Meta:
        model = MailingList
        fields = ['owner', 'name']
