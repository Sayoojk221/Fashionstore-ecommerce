# Generated by Django 3.1 on 2020-10-05 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_auto_20201005_1932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productreview',
            old_name='productid',
            new_name='colorid',
        ),
    ]
