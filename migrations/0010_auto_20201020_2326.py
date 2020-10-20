# Generated by Django 3.1.2 on 2020-10-20 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0009_delete_projectimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.CharField(blank=True, choices=[('RES', 'Residenziale'), ('TER', 'Terziario'), ('SAN', 'Sanitario'), ('PRO', 'Produttivo')], max_length=4, null=True, verbose_name='Categoria funzionale'),
        ),
        migrations.AddField(
            model_name='project',
            name='cost',
            field=models.CharField(blank=True, choices=[('1K', '1K'), ('10K', '10K'), ('100K', '100K'), ('1M', '1M'), ('10M', '10M')], max_length=4, null=True, verbose_name="Costo dell'intervento"),
        ),
        migrations.AddField(
            model_name='project',
            name='site',
            field=models.CharField(blank=True, help_text='Va bene tipo "Roma - Monteverde"', max_length=100, null=True, verbose_name='Luogo'),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('INP', 'In corso di progettazione'), ('PRO', 'Progettato'), ('INC', 'In corso di costruzione'), ('COS', 'Costruito'), ('IND', 'In corso di demolizione'), ('DEM', 'Demolito')], max_length=4, null=True, verbose_name="Stato dell'intervento"),
        ),
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.CharField(blank=True, choices=[('ARR', 'Arredamento'), ('RIS', 'Ristrutturazione'), ('RES', 'Restauro'), ('AMP', 'Ampliamento'), ('COS', 'Costruzione'), ('DEM', 'Demolizione')], max_length=4, null=True, verbose_name='Tipo di intervento'),
        ),
    ]
