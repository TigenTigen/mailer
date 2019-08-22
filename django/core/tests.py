from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model

from rest_framework import APITestCase

from mailinglist.models import Subscriber, MailingList
from mailinglist.factories import SubscriberFactory

class MockSendEmailToSubscriberTask:
    def setUp(self):
        self.send_confirmation_email_patch = patch('mailinglist.tasks.send_confirmation_email_to_subscriber')
        self.send_confirmation_email_mock = self.send_confirmation_email_patch.start()
        super().setUp()

    def tearDown(self):
        self.send_confirmation_email_patch.stop()
        self.send_confirmation_email_mock = None
        super().tearDown()

class SubscriberCreationTestCase(MockSendEmailToSubscriberTask, TestCase):
    def test_calling_create_queues_confirmation_email_task(self):
        user = get_user_model().objects.create_user(username='unit test runner')
        mailinglist = MailingList.objects.create(name='unit test', owner=user)
        Subscriber.objects.create(email='unittest@example.com', mailinglist=mailinglist)
        self.assertEqual(self.send_confirmation_email_mock.delay.call_count, 1)

class SubscriberManagerTastCase(TestCase):
    def testConfirmedSubscriberForMailinglist(self):
        mailinglist = MailingList.objects.create(
            name='unit test',
            owner=get_user_model().objects.create_user(username='unit test'))
        confirmed_users = [SubscriberFactory(confirmed=True, mailinglist=mailinglist) for n in range(3)]
        unconfirmed_users = [SubscriberFactory(mailinglist=mailinglist) for n in range(3)]
        confirmed_users_queryset = Subscriber.objects.confirmed_subscribers_from_mailinglist(mailinglist=mailinglist)
        self.assertEqual(len(confirmed_users), confirmed_users_queryset.count())
        for user in confirmed_users_queryset:
            self.assertIn(user, confirmed_users)

class ListMailinglistWithAPITastCase(APITestCase):
    def setUp(self):
        password = 'password'
        username = 'unit test'
        self.user = get_user_model().objects.create_user(username=username, password=password)
        cred_bytes = '{}:{}'.format(username, password).encode('utf-8')
        self.basic_auth = base64.b64encode(cred_bytes).decode('utf-8')

    def test_listing_my_mailinglists(self):
        mailinglists = [
            MailingList.objects.create(name='unit test {}'.format(i), owner=self.user) for i in range(3)
        ]
        self.client.credentials(HTTP_AUTHORIZATION='Basic {}'.format(self.basic_auth))
        response = self.client.get('api/v1/mailinglist')
        self.assertEqual(200, response.status_code)
        parsed = json.loads(response.content)
        self.assertEqual(3, len(parsed))
        content = str(response.content)
        for mailinglist in mailinglist:
            self.assertIn(str(mailinglist.id), content)
            self.assertIn(str(mailinglist.name), content)
