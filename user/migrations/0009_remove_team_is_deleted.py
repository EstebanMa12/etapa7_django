# Generated by Django 5.0 on 2023-12-15 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_customuser_managers_alter_customuser_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='is_deleted',
        ),
    ]