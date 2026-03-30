from django.contrib.admin.filters import SimpleListFilter

from .dropdown import DropdownMixin


class CustomQuerysetFilter(DropdownMixin, SimpleListFilter):

    pass
