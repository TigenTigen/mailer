from rest_framework.permissions import BasePermission

from core.models import MailingList, Subscriber

class CanUseMailinglist(BasePermission):
    message = 'Доступ к данному ресурсу для Вас невозможен'

    def has_object_permission(self, request, view, object):
        user = request.user
        if isinstance(object, Subscriber):
            return object.mailinglist.user_can_use_mailinglist(user)
        elif isinstance(object, MailingList):
            return object.user_can_use_mailinglist(user)
        return False
