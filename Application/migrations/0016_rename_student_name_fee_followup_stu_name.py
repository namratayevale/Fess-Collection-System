# Generated by Django 5.0.1 on 2024-04-06 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0015_alter_fee_followup_student_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fee_followup',
            old_name='student_name',
            new_name='stu_name',
        ),
    ]