# Generated by Django 5.0 on 2023-12-12 22:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_comment_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.team'),
        ),
    ]
