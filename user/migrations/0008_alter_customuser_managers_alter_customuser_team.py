# Generated by Django 5.0 on 2023-12-15 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_customuser_is_admin'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.team'),
        ),
    ]
