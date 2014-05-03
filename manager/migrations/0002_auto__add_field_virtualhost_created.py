# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'VirtualHost.created'
        db.add_column('manager_virtualhost', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 18, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'VirtualHost.created'
        db.delete_column('manager_virtualhost', 'created')


    models = {
        'manager.virtualhost': {
            'Meta': {'object_name': 'VirtualHost'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 18, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'db_password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['manager']