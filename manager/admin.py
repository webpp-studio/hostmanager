from django.contrib import admin
from django import forms

from manager.models import VirtualHost


class VirtualHostAdmin(admin.ModelAdmin):
    fields = ['site_name', 'domain', 'username',
              'password', 'db_password', 'description', 'is_active']
    list_display = ['site_name', 'domain', 'is_active']
    list_filter = ['created']
    search_fields = ['domain', 'site_name']
    ordering = ['-created']

    class form(forms.ModelForm):
        class Meta:
            models = VirtualHost
            widgets = {
                'site_name': forms.TextInput(attrs={'size': 80}),
                'description': forms.Textarea(attrs={'cols': 50, 'rows': 10})
            }


admin.site.register(VirtualHost, VirtualHostAdmin)
