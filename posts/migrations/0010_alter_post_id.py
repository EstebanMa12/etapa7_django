# Generated by Django 5.0 on 2023-12-21 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=None, editable=False, primary_key=True, serialize=False),
        ),
    ]