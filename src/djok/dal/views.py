import operator
from functools import reduce

from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView as View
from django.db.models import Q
from queryset_sequence import QuerySetSequence

__all__ = ['Select2QuerySetSequenceAutoView']


class Select2QuerySetSequenceAutoView(View):

    def get_queryset(self):
        """Return queryset."""
        queryset_models = []
        for model_args in self.model_choice:
            model = model_args[0]
            filter_value = model_args[1]

            if ' ' in self.q:
                and_q = []
                for bit in self.q.strip().split(' '):
                    and_q.append(Q(**{f'{filter_value}__icontains': bit}))

                forward_filtered = [reduce(operator.and_, and_q)]
            else:
                kwargs_model = {
                    f'{filter_value}__icontains': self.q if self.q else ''
                }
                forward_filtered = [Q(**kwargs_model)]

            try:
                forward_fields = model_args[2]
                for forward in forward_fields:
                    field_key = '{}__icontains'.format(forward[1])
                    field_value = self.forwarded[forward[0]]
                    forward_filtered.append(Q(**{field_key: field_value}))
            except IndexError:
                # if no list on the 3rd index of self.model_choice
                # (reserved for forwarding fields)
                pass

            # link the different field by an & query
            and_forward_filtered = reduce(lambda x, y: x & y, forward_filtered)

            queryset_models.append(model.objects.filter(and_forward_filtered))

        # Aggregate querysets
        qs = QuerySetSequence(*queryset_models)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs
