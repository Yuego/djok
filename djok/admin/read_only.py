from django.contrib import admin

__all__ = ['ReadOnlyAdminMixin']


class ReadOnlyAdminMixin:
    """
    Миксин, отключающий возможность редактирования записей
    """

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request) -> bool:
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_delete_link'] = False
        extra_context['show_save'] = False
        extra_context['show_save_as_new'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False

        return super().change_view(request=request, object_id=object_id,
                                   form_url=form_url, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None) -> tuple:
        rof = tuple(super().get_readonly_fields(request=request, obj=obj))

        rof += tuple([f.name for f in self.model._meta.get_fields(include_parents=True)])

        return rof
