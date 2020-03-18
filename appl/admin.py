from django.contrib import admin

# Register your models here.
from django.forms import ClearableFileInput
from django.db import models

from appl.models import Static, StaticContentAttachments, StaticCategories


# class MyAdminSite(admin.AdminSite):
#     site_header = 'Monty Python administration'
#
#
# admin_site = MyAdminSite(name='myadmin')
#

class AttachmentsClearableFileInput(ClearableFileInput):
    template_name = 'appl/admin/clearable_file_input.html'


class StaticContentAttachmentsInline(admin.StackedInline):
    model = StaticContentAttachments
    extra = 1
    formfield_overrides = {
        models.FileField: {'widget': AttachmentsClearableFileInput},
    }
    # class Meta:
    #     widgets = {
    #         'file': MyClearableFileInput(),
    #     }


@admin.register(StaticCategories)
class StaticCategoriesAdmin(admin.ModelAdmin):
    # pass
    # fields = ('name',)
    search_fields = ('name',)

    #   Проверить если user не админ,
    #   запретить редактирование
    def has_add_permission(self, request):
        return request.user.is_staff or False

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff or False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff or False


@admin.register(Static)
class StaticAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'start']
    fieldsets = [
        (None, {'fields': ['category', 'title', 'icon', 'short', 'content']}),
    ]
    # readonly_fields = ('category',)
    inlines = [StaticContentAttachmentsInline]

    autocomplete_fields = ('category',)
