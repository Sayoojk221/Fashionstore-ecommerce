# Generated by Django 3.1 on 2020-10-01 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_orderlist_deliverystatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeraddress',
            name='phone',
            field=models.CharField(default='', max_length=200),
        ),
    ]
