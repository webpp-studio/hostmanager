from django.db import models
from django.contrib.auth.models import User


class ActiveVirtualHostManager(models.Manager):
    def get_query_set(self):
        return super(ActiveVirtualHostManager, self).get_query_set()\
                .filter(is_active=True).order_by('created')


class InactiveVirtualHostManager(models.Manager):
    def get_query_set(self):
        return super(InactiveVirtualHostManager, self).get_query_set()\
                .exclude(is_active=True).order_by('created')


class VirtualHost(models.Model):
    '''
    Availible virtual hosts
    '''
    site_name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)
    domain = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    db_password = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    enabled = ActiveVirtualHostManager()
    disabled = InactiveVirtualHostManager()

    def __unicode__(self):
        return self.site_name
