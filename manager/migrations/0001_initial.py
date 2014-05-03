# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VirtualHost'
        db.create_table('manager_virtualhost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('db_password', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('manager', ['VirtualHost'])


    def backwards(self, orm):
        # Deleting model 'VirtualHost'
        db.delete_table('manager_virtualhost')


    models = {
        'manager.virtualhost': {
            'Meta': {'object_name': 'VirtualHost'},
            'db_password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['manager']