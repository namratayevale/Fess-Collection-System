# Generated by Django 5.0.1 on 2024-03-14 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0002_location_master'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]
