# Generated by Django 5.0.1 on 2024-03-20 06:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0009_stu_admit'),
    ]

    operations = [
        migrations.AddField(
            model_name='stu_admit',
            name='duration',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='stu_admit',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Application.subcategory_master'),
        ),
    ]
