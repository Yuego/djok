from django.contrib.admin.filters import (
    SimpleListFilter,
    AllValuesFieldListFilter,
    ChoicesFieldListFilter,
    RelatedFieldListFilter,
    RelatedOnlyFieldListFilter
)
class DropdownMixin:
    template = 'djok/admin/dropdown_filter.html'

class SimpleDropdownFilter(DropdownMixin, SimpleListFilter):
    pass


class DropdownFilter(DropdownMixin,  AllValuesFieldListFilter):
    pass


class ChoiceDropdownFilter(DropdownMixin,  ChoicesFieldListFilter):
    pass


class RelatedDropdownFilter(DropdownMixin,  RelatedFieldListFilter):
    pass


class RelatedOnlyDropdownFilter(DropdownMixin,  RelatedOnlyFieldListFilter):
    pass
