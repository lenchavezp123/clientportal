# Generated by Django 3.2.5 on 2022-03-12 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_vat'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='zip',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
