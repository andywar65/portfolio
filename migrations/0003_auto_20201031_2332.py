# Generated by Django 3.1.2 on 2020-10-31 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_auto_20201031_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectstation',
            name='prog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_station', to='portfolio.project'),
        ),
    ]
