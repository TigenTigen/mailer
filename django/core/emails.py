from django.conf import settings
from django.template import Context, engines
from django.core.mail import send_mail
from django.utils.datetime_safe import datetime
from django.urls import reverse
from datetime import datetime

CONFIRM_SUBSCRIPTION_HTML = 'emails/subscription_confirmation.html'
CONFIRM_SUBSCRIPTION_TXT = 'emails/subscription_confirmation.txt'

SUBSCRIBER_MASSAGE_HTML = 'emails/subscriber_massage.html'
SUBSCRIBER_MASSAGE_TXT = 'emails/subscriber_massage.txt'

class EmailTemplateContext(Context):

    @staticmethod
    def make_link(path):
        return settings.MAILING_LIST_LINK_DOMAIN + path

    def common_context(self, subscriber):
        return {
            'subscriber': subscriber,
            'mailinglist': subscriber.mailinglist,
            'unsubscribtion_link': self.make_link(reverse('core:unsubscribe', kwargs={'pk': subscriber.id}))
        }

    def __init__(self, subscriber, dict_=None, **kwargs):
        if dict_ is None:
            dict_ = {}
        email_context = self.common_context(subscriber)
        email_context.update(dict_)
        super().__init__(email_context, **kwargs)

def send_confirmation_email(subscriber):
    mailinglist = subscriber.mailinglist
    confirmation_link = EmailTemplateContext.make_link(reverse('core:confirm_subscription', kwargs={'pk': subscriber.id}))
    context = EmailTemplateContext(subscriber, {'confirmation_link': confirmation_link})
    subject = 'Подтверждение подписки на список рассылки "{}"'.format(mailinglist.name)
    dt_engine = engines['django'].engine
    text_body = dt_engine.get_template(CONFIRM_SUBSCRIPTION_TXT).render(context=context)
    html_body = dt_engine.get_template(CONFIRM_SUBSCRIPTION_HTML).render(context=context)
    send_mail(
        subject=subject,
        message=text_body,
        from_email=settings.MAILING_LIST_FROM_EMAIL,
        recipient_list=[subscriber.email,],
        html_message=html_body)

def send_massage(subscriber_massage):
    massage = subscriber_massage.massage
    context = EmailTemplateContext(subscriber_massage.subscriber, {'body': massage.body})
    dt_engine = engines['django'].engine
    text_body = dt_engine.get_template(SUBSCRIBER_MASSAGE_TXT).render(context=context)
    html_body = dt_engine.get_template(SUBSCRIBER_MASSAGE_HTML).render(context=context)
    utcnow = datetime.utcnow()
    subscriber_massage.last_attempt = utcnow
    subscriber_massage.save()
    success = send_mail(
        subject=massage.subject,
        message=text_body,
        from_email=settings.MAILING_LIST_FROM_EMAIL,
        recipient_list=[subscriber_massage.subscriber.email,],
        html_message=html_body)
    if success == 1:
        subscriber_massage.sent = utcnow
        subscriber_massage.save()
        massage.refresh_finish_data()
        if massage.started == None:
            massage.started = utcnow
            massage.save()
