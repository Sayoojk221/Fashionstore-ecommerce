# Generated by Django 3.1 on 2020-09-28 06:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colorid', models.CharField(default='', max_length=200)),
                ('productpicture', models.ImageField(default='', upload_to='product')),
                ('picture', models.ImageField(default='', upload_to='product')),
                ('picture2', models.ImageField(default='', upload_to='product')),
                ('picture3', models.ImageField(default='', upload_to='product')),
                ('color', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCommon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.CharField(default='', max_length=200)),
                ('title', models.CharField(default='', max_length=200)),
                ('gender', models.CharField(default='', max_length=200)),
                ('productdetail', models.CharField(default='', max_length=1000)),
                ('stylenote', models.CharField(default='', max_length=2000)),
                ('shippingandreturns', models.CharField(default='', max_length=500)),
                ('createddate', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(default='', max_length=50)),
                ('password', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sizeid', models.CharField(default='', max_length=200)),
                ('size', models.CharField(default='', max_length=200)),
                ('quantity', models.IntegerField()),
                ('price', models.CharField(default='', max_length=200)),
                ('productcolor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminpanel.productcolor')),
            ],
        ),
        migrations.CreateModel(
            name='ProductLists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.CharField(default='', max_length=200)),
                ('productfulldetails', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminpanel.productsize')),
            ],
        ),
        migrations.AddField(
            model_name='productcolor',
            name='productcommon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminpanel.productcommon'),
        ),
    ]
