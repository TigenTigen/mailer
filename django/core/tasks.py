from celery import shared_task
from core.emails import send_confirmation_email, send_massage
import uuid

@shared_task
def send_confirmation_email_to_subscriber(subscriber_id):
    from core.models import Subscriber
    subscriber = Subscriber.objects.get(id=subscriber_id)
    send_confirmation_email(subscriber)

@shared_task
def building_subscriber_massage_from_massage(massage_id):
    from core.models import Massage, SubscriberMassage
    massage = Massage.objects.get(id=massage_id)
    SubscriberMassage.objects.create_from_massage(massage)

@shared_task
def send_subscriber_massage(subscriber_massage_id):
    from core.models import SubscriberMassage
    subscriber_massage = SubscriberMassage.objects.get(id=subscriber_massage_id)
    send_massage(subscriber_massage)
