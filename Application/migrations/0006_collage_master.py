# Generated by Django 5.0.1 on 2024-03-18 05:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0005_university_master'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collage_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collage', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Application.university_master')),
            ],
        ),
    ]
