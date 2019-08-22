from django.core.exceptions import PermissionDenied, FieldDoesNotExist
from core.models import MailingList

class UserCanUseMailingList:
    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        user = self.request.user
        if isinstance(object, MailingList):
            if object.user_can_use_mailinglist(user):
                return object
            else:
                raise PermissionDenied()
        mailinglist_attr = getattr(object, 'mailinglist')
        if isinstance(mailinglist_attr, MailingList):
            if mailinglist_attr.user_can_use_mailinglist(user):
                return object
            else:
                raise PermissionDenied()
        raise FieldDoesNotExist()
