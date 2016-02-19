# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-12 22:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('standards_review', '0005_auto_20160112_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='FragmentationSpectrum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precursor_mz', models.FloatField(null=True)),
                ('_centroid_mzs', models.TextField()),
                ('_centroid_ints', models.TextField()),
                ('spec_num', models.IntegerField()),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standards_review.Dataset')),
                ('standard', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='standards_review.Standard')),
            ],
        ),
    ]