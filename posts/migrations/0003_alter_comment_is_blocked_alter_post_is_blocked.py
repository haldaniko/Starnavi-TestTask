# Generated by Django 5.1.2 on 2024-10-19 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
