# Generated by Django 4.0.3 on 2022-04-15 10:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0004_remove_project_last_updated_project_client_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="slug_de",
            field=models.SlugField(
                blank=True,
                help_text="Appears on the address bar",
                max_length=100,
                null=True,
                verbose_name="Slug",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="slug_it",
            field=models.SlugField(
                blank=True,
                help_text="Appears on the address bar",
                max_length=100,
                null=True,
                verbose_name="Slug",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="Start date"
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Appears on the address bar",
                max_length=100,
                null=True,
                verbose_name="Slug",
            ),
        ),
    ]