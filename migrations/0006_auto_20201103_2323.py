# Generated by Django 3.1.2 on 2020-11-03 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_auto_20201101_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationimage',
            name='image',
            field=models.ImageField(max_length=200, null=True, upload_to='uploads/images/galleries/', verbose_name='Immagine'),
        ),
        migrations.AlterField(
            model_name='stationimage',
            name='stat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='station_image', to='portfolio.projectstation', verbose_name='Stazione'),
        ),
    ]