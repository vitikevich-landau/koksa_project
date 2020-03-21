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

    def get_model_perms(self, request):
        return {}


@admin.register(Static)
class StaticAdmin(admin.ModelAdmin):
    change_form_template = 'appl/admin/change_form.html'

    list_display = ['title', 'category', 'start']
    fieldsets = [
        (None, {'fields': ['category', 'title', 'icon', 'short', 'content']}),
    ]
    # readonly_fields = ('category',)
    inlines = [StaticContentAttachmentsInline]

    autocomplete_fields = ('category',)
