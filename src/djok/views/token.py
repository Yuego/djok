import datetime

from django.db.models import F
from django.views.generic import DetailView

from djok.models.token_base import TokenBase

__all__ = ['TokenViewBase']


class TokenViewBase(DetailView):
    slug_field = 'uid'
    slug_url_kwarg = 'token'

    confirm_field = 'uid2'
    confirm_url_kwarg = 'token2'

    object: TokenBase

    def success(self, request, *args, **kwargs):
        raise NotImplementedError

    def fail(self, request, *args, **kwargs):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        token: TokenBase
        token = self.object = self.get_object()

        confirm = kwargs[self.confirm_url_kwarg]
        confirm_check = getattr(token, self.confirm_field)

        if confirm != confirm_check:
            return self.fail(request, *args, **kwargs)

        today = datetime.date.today()

        if today > self.object.expire:
            return self.fail(request, *args, **kwargs)

        else:
            if 0 < token.usage_limit <= token.current_usage:
                return self.fail(request, *args, **kwargs)

            token.current_usage = F('current_usage') + 1
            token.save(update_fields=['current_usage'])

            return self.success(request, *args, **kwargs)
