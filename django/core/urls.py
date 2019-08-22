from django.urls import path

from core import views

app_name = 'core'
urlpatterns = [
    path('', views.MailingListListView.as_view(), name='my_mailinglist_list'),
    path('new', views.MailingListCreateView.as_view(), name='create_mailinglist'),
    path('<uuid:pk>/delete', views.MailingListDeleteView.as_view(), name='delete_mailinglist'),
    path('<uuid:pk>/manage', views.MailingListDetailView.as_view(), name='manage_mailinglist'),
    path('<uuid:mailinglist_id>/subscribe', views.SubscriberCreateView.as_view(), name='subscribe_to_mailinglist'),
    path('<uuid:pk>/thankyou', views.ThankyouForSubscribeView.as_view(), name='thankyou_for_subscribtion'),
    path('subscribe/confirmation/<uuid:pk>', views.ConfirmSubscriptionView.as_view(), name='confirm_subscription'),
    path('unsubscribe/<uuid:pk>', views.SubscriberDeleteView.as_view(), name='unsubscribe'),
    path('<uuid:mailinglist_id>/massage/new', views.MassageCreateView.as_view(), name='create_massage'),
    path('massage/<uuid:pk>', views.MassageDetailView.as_view(), name='view_massage'),
    #API section:
    path('api/v1/mailinglist', views.MailingListCreateListView.as_view(), name='api-mailinglist-list'),
    path('api/v1/mailinglist/<uuid:pk>', views.MailingListRetrieveUpdateDestroyView.as_view(), name='api-mailinglist-detail'),
    path('api/v1/mailinglist/<uuid:mailinglist_pk>/subscribers', views.SubscriberListCreateView.as_view(), name='api-subscriber-list'),
    path('api/v1/subscriber/<uuid:pk>', views.SubscriberRetrieveUpdateDestroyView.as_view(), name='api-subscriber-detail'),
]
