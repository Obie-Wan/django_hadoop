# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CommonJob'
        db.create_table(u'django_hadoop_commonjob', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hadoop_job_id', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='NEW', max_length=16)),
            ('priority', self.gf('django.db.models.fields.CharField')(default='NORMAL', max_length=16)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'django_hadoop', ['CommonJob'])


    def backwards(self, orm):
        # Deleting model 'CommonJob'
        db.delete_table(u'django_hadoop_commonjob')


    models = {
        u'django_hadoop.commonjob': {
            'Meta': {'object_name': 'CommonJob'},
            'hadoop_job_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'NORMAL'", 'max_length': '16'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NEW'", 'max_length': '16'})
        }
    }

    complete_apps = ['django_hadoop']