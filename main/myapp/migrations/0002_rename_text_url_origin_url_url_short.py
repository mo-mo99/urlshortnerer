# Generated by Django 4.0.4 on 2022-05-25 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='text',
            new_name='origin_url',
        ),
        migrations.AddField(
            model_name='url',
            name='short',
            field=models.CharField(default='0', max_length=10),
        ),
    ]