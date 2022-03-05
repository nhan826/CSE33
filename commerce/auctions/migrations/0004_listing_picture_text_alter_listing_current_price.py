# Generated by Django 4.0.2 on 2022-03-04 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='picture_text',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='current_price',
            field=models.FloatField(),
        ),
    ]
