# Generated by Django 4.0.4 on 2022-06-22 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_url_hash_salted_url_alter_url_salt'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='visited',
            field=models.IntegerField(default=0),
        ),
    ]
