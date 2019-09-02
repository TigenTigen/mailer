from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from core.models import *
from core.forms import *
from core.mixins import *

# MailingList views

class MailingListListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)

class MailingListCreateView(LoginRequiredMixin, CreateView):
    form_class = MailingListForm
    template_name = 'core/mailinglist_form.html'

    def get_initial(self):
        return {'owner': self.request.user.id}

class MailingListDeleteView(LoginRequiredMixin, UserCanUseMailingList, DeleteView):
    model = MailingList
    success_url = reverse_lazy('core:my_mailinglist_list')

class MailingListDetailView(LoginRequiredMixin, UserCanUseMailingList, DetailView):
    model = MailingList

# Subscription views

class SubscriberCreateView(LoginRequiredMixin, CreateView):
    form_class = SubscriberForm
    template_name = 'core/subscriber_form.html'

    def get_initial(self):
        return {'mailinglist': self.kwargs['mailinglist_id']}

    def get_success_url(self):
        return reverse('core:thankyou_for_subscribtion', kwargs={'pk': self.object.mailinglist.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailinglist_id = self.kwargs['mailinglist_id']
        context['mailinglist'] = get_object_or_404(MailingList, id=mailinglist_id)
        return context

class ThankyouForSubscribeView(DetailView):
    model = MailingList
    template_name = 'core/thankyou_for_subscribe.html'

class ConfirmSubscriptionView(DetailView):
    model = Subscriber
    template_name = 'core/subscriber_confirmation.html'

    def get_object(self, queryset=None):
        subscriber = super().get_object(queryset=queryset)
        subscriber.confirmed = True
        subscriber.save()
        return subscriber

class SubscriberDeleteView(DeleteView):
    model = Subscriber

    def get_success_url(self):
        mailinglist_id = self.object.mailinglist.id
        return reverse('core:subscribe_to_mailinglist', args=[mailinglist_id,])

# Massage views

class MassageCreateView(LoginRequiredMixin, CreateView):
    SAVE_ACTION = 'save'
    PREVIEW_ACTION = 'preview'

    form_class = MassageForm
    template_name = 'core/massage_form.html'

    def get_mailinglist(self):
        mailinglist = get_object_or_404(MailingList, id=self.kwargs['mailinglist_id'])
        if not mailinglist.user_can_use_mailinglist(self.request.user):
            raise PermissionDenied()
        return mailinglist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailinglist = self.get_mailinglist()
        context.update({
            'mailinglist': mailinglist,
            'SAVE_ACTION': self.SAVE_ACTION,
            'PREVIEW_ACTION': self.PREVIEW_ACTION,
        })
        return context

    def get_initial(self):
        mailinglist = self.get_mailinglist()
        return {'mailinglist': mailinglist.id}

    def get_success_url(self):
        return reverse('core:manage_mailinglist', kwargs={'pk': self.object.mailinglist.id})

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == self.PREVIEW_ACTION:
            context = self.get_context_data(form=form, massage=form.instance)
            return self.render_to_response(context=context)
        else:
            return super().form_valid(form)

class MassageDetailView(LoginRequiredMixin, UserCanUseMailingList, DetailView):
    model = Massage

# API section
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.permissions import *
from core.serializers import *

class MailingListCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, CanUseMailinglist)
    serializer_class = MailingListSerialazer

    def get_queryset(self):
        return self.request.user.mailinglist_set.all()

    def get_serializer(self, *args, **kwargs):
        if kwargs.get('data', None):
            data = kwargs.get('data', None)
            owner = {'owner': self.request.user.id}
            data.update(owner)
        return super().get_serializer(*args, **kwargs)

class MailingListRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, CanUseMailinglist)
    serializer_class = MailingListSerialazer
    queryset = MailingList.objects.all()

class SubscriberListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, CanUseMailinglist)
    serializer_class = SubscriberSerialazer

    def get_queryset(self):
        mailinglist_pk = self.kwargs['mailinglist_pk']
        mailinglist = get_object_or_404(MailingList, id=mailinglist_pk)
        return mailinglist.subscriber_set.all()

    def get_serializer(self, *args, **kwargs):
        if kwargs.get('data'):
            data = kwargs.get('data')
            mailinglist = {
                'mailinglist': reverse(
                    'core:api-mailinglist-detail',
                    kwargs={'pk': self.kwargs['mailinglist_pk']})
            }
            data.update(mailinglist)
        return super().get_serializer(*args, **kwargs)

class SubscriberRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, CanUseMailinglist)
    serializer_class = ReadOnlyEmailSubscriberSerialazer
    queryset = Subscriber.objects.all()

class MassageListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, CanUseMailinglist)
    serializer_class = MassageSerialazer

    def get_queryset(self):
        mailinglist_pk = self.kwargs['mailinglist_pk']
        mailinglist = get_object_or_404(MailingList, id=mailinglist_pk)
        return mailinglist.massage_set.all()

    def get_serializer(self, *args, **kwargs):
        if kwargs.get('data'):
            data = kwargs.get('data')
            mailinglist = {
                'mailinglist': reverse(
                    'core:api-mailinglist-detail',
                    kwargs={'pk': self.kwargs['mailinglist_pk']})
            }
            data.update(mailinglist)
        return super().get_serializer(*args, **kwargs)
