# Generated by Django 4.1 on 2022-09-09 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_user_listing_owner_rename_name_listing_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]