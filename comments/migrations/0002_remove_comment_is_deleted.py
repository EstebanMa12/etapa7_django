# Generated by Django 5.0 on 2023-12-15 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_deleted',
        ),
    ]
