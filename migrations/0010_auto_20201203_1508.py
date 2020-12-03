# Generated by Django 3.1.2 on 2020-12-03 14:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0009_auto_20201129_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='map',
            field=models.JSONField(blank=True, null=True, verbose_name='Map overlay'),
        ),
        migrations.AlterField(
            model_name='projectstation',
            name='lat',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='projectstation',
            name='long',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude'),
        ),
        migrations.CreateModel(
            name='ProjectMapDxf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=200, upload_to='uploads/projects/maps/dxf/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['dxf'])], verbose_name='DXF file')),
                ('prog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectmap_dxf', to='portfolio.project', verbose_name='Project')),
            ],
        ),
    ]
