# Generated by Django 4.0.2 on 2022-02-19 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortner', '0002_rename_user_id_urllist_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='urllist',
            name='total_clicks',
            field=models.IntegerField(default=0),
        ),
    ]
