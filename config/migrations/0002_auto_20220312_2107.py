# Generated by Django 3.2.5 on 2022-03-12 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminbase',
            name='cookies',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='adminbase',
            name='cookies_text',
            field=models.TextField(blank=True),
        ),
    ]
