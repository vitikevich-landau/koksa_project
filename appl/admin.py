from django.contrib import admin

# Register your models here.
from django.forms import ClearableFileInput
from django.db import models

from appl.models import Static, StaticContentAttachments


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


class StaticAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'start']
    fieldsets = [
        (None, {'fields': ['category', 'title', 'icon', 'short', 'content']}),
    ]
    inlines = [StaticContentAttachmentsInline]


admin.site.register(Static, StaticAdmin)