# Generated by Django 4.0.4 on 2022-06-22 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_url_hash_salted_url_alter_url_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='hash_salted_url',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='url',
            name='salt',
            field=models.CharField(max_length=1000),
        ),
    ]