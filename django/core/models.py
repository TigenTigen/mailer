import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.tasks import send_confirmation_email_to_subscriber, building_subscriber_massage_from_massage, send_subscriber_massage

USER_MODEL = get_user_model()

class MailingList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Наименование', max_length=100)
    owner = models.ForeignKey(to=USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:manage_mailinglist', kwargs={'pk': self.id})

    def user_can_use_mailinglist(self, user):
        return user == self.owner

class SubscriberManager(models.Manager):
    def confirmed_subscribers_from_mailinglist(self, mailinglist):
        queryset = self.get_queryset()
        queryset = queryset.filter(confirmed=True)
        queryset = queryset.filter(mailinglist=mailinglist)
        return queryset

class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField('Адрес электронной почты')
    confirmed = models.BooleanField(default=False)
    mailinglist = models.ForeignKey(to=MailingList, on_delete=models.CASCADE)

    objects = SubscriberManager()

    class Meta:
        unique_together = ['email', 'mailinglist']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_new = self._state.adding or force_insert
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if is_new and not self.confirmed:
            self.send_confirmation_email()

    def send_confirmation_email(self):
        send_confirmation_email_to_subscriber.delay(self.id)

class Massage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mailinglist = models.ForeignKey(to=MailingList, on_delete=models.CASCADE)
    subject = models.CharField('Тема сообщения', max_length=100)
    body = models.TextField('Текст сообщения')
    started = models.DateTimeField(default=None, null=True)
    finished = models.DateTimeField(default=None, null=True)

    class Meta:
        ordering = ['-started']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_new = self._state.adding or force_insert
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if is_new:
            building_subscriber_massage_from_massage.delay(self.id)

    def refresh_finish_data(self):
        messages_to_send = Subscriber.objects.confirmed_subscribers_from_mailinglist(self.mailinglist).count()
        messages_sent = self.subscribermassage_set.filter(sent__isnull=False)
        if messages_sent.count() == messages_to_send:
            last_message = messages_sent.order_by('sent').last()
            self.finished = last_message.sent
            self.save()

class SubscriberMassageManager(models.Manager):
    def create_from_massage(self, massage):
        confirmed_subscribers = Subscriber.objects.confirmed_subscribers_from_mailinglist(massage.mailinglist)
        return [self.create(massage=massage, subscriber=subscriber) for subscriber in confirmed_subscribers]

class SubscriberMassage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    massage = models.ForeignKey(to=Massage, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(to=Subscriber, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(default=None, null=True)
    last_attempt = models.DateTimeField(default=None, null=True)

    objects = SubscriberMassageManager()

    class Meta:
        ordering = ['-sent']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_new = self._state.adding or force_insert
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if is_new:
            send_subscriber_massage.delay(self.id)
