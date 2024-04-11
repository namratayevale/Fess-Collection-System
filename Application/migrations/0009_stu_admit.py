# Generated by Django 5.0.1 on 2024-03-20 05:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0008_stu_inquiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stu_Admit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadhar_no', models.CharField(blank=True, max_length=13, null=True)),
                ('date', models.DateField()),
                ('total_fees', models.IntegerField(blank=True, default=0, null=True)),
                ('paid_now', models.IntegerField(blank=True, default=0, null=True)),
                ('balance_fees', models.IntegerField(blank=True, default=0, null=True)),
                ('system', models.CharField(blank=True, max_length=30, null=True)),
                ('next_followup_date', models.DateField()),
                ('fee_close', models.CharField(blank=True, max_length=10, null=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Application.course_master')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Application.location_master')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Application.stu_inquiry')),
            ],
        ),
    ]