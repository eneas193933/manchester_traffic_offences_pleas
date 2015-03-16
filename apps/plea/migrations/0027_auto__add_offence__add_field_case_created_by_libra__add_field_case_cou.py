# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Offence'
        db.create_table(u'plea_offence', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('case', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plea.Case'])),
            ('offence_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('offence_title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('offence_wording', self.gf('django.db.models.fields.TextField')()),
            ('offence_sequence_number', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'plea', ['Offence'])

        # Adding field 'Case.created_by_libra'
        db.add_column(u'plea_case', 'created_by_libra',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Case.court'
        db.add_column(u'plea_case', 'court',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plea.Court'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Offence'
        db.delete_table(u'plea_offence')

        # Deleting field 'Case.created_by_libra'
        db.delete_column(u'plea_case', 'created_by_libra')

        # Deleting field 'Case.court'
        db.delete_column(u'plea_case', 'court_id')


    models = {
        u'plea.case': {
            'Meta': {'object_name': 'Case'},
            'court': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plea.Court']", 'null': 'True', 'blank': 'True'}),
            'created_by_libra': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'created_not_sent'", 'max_length': '30'}),
            'status_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'urn': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'})
        },
        u'plea.court': {
            'Meta': {'object_name': 'Court'},
            'court_address': ('django.db.models.fields.TextField', [], {}),
            'court_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'court_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'court_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'court_telephone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plp_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'submission_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'test_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'plea.courtemailcount': {
            'Meta': {'object_name': 'CourtEmailCount'},
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hearing_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sc_guilty_char_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sc_not_guilty_char_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'status_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'total_guilty': ('django.db.models.fields.IntegerField', [], {}),
            'total_not_guilty': ('django.db.models.fields.IntegerField', [], {}),
            'total_pleas': ('django.db.models.fields.IntegerField', [], {})
        },
        u'plea.offence': {
            'Meta': {'object_name': 'Offence'},
            'case': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plea.Case']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offence_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'offence_sequence_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'offence_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'offence_wording': ('django.db.models.fields.TextField', [], {})
        },
        u'plea.usagestats': {
            'Meta': {'ordering': "('start_date',)", 'object_name': 'UsageStats'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'online_guilty_pleas': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'online_not_guilty_pleas': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'online_submissions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'postal_requisitions': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'postal_responses': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['plea']