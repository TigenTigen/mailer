from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import MailingList, Subscriber

class MailingListSerialazer(serializers.HyperlinkedModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = MailingList
        fields = ('url', 'id', 'name', 'subscriber_set', 'owner')
        read_only_fields = ('subscriber_set',)
        extra_kwargs = {
            'url': {'view_name': 'core:api-mailinglist-detail'},
            'subscriber_set': {'view_name': 'core:api-subscriber-detail'},
        }

class SubscriberSerialazer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('url', 'id', 'email', 'confirmed', 'mailinglist')
        extra_kwargs = {
            'url': {'view_name': 'core:api-subscriber-detail'},
            'mailinglist': {'view_name': 'core:api-mailinglist-detail'},
        }

class ReadOnlyEmailSubscriberSerialazer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('url', 'id', 'email', 'confirmed', 'mailinglist')
        read_only_fields = ('email', 'mailinglist')
        extra_kwargs = {
            'url': {'view_name': 'core:api-subscriber-detail'},
            'mailinglist': {'view_name': 'core:api-mailinglist-detail'},
        }
